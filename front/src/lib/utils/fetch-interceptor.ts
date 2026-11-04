import { browser } from "$app/environment";
import { NETWORK_ERROR_MESSAGES, RATE_LIMIT_MESSAGE } from "$lib/consts";
import { API_URL } from "$lib/env";
import * as Sentry from "@sentry/sveltekit";
import { toast } from "@zerodevx/svelte-toast";

/**
 * Détermine si une requête est à destination de notre propre site.
 * Les requêtes émises par des scripts tiers (Google CSE, etc.) passent
 * aussi par l'intercepteur, mais leurs échecs réseau (bloqueurs de pub,
 * réseau instable…) ne doivent pas être remontés à Sentry.
 */
function isFirstPartyRequest(input: string | URL | Request): boolean {
  try {
    const rawUrl = input instanceof Request ? input.url : input.toString();
    const url = new URL(rawUrl, window.location.href);
    return (
      url.origin === window.location.origin || url.href.startsWith(API_URL)
    );
  } catch {
    return false;
  }
}

/**
 * Un échec réseau brut (aucune réponse reçue) n'apporte aucune information
 * exploitable : il est provoqué par l'environnement du client (bloqueur de pub,
 * perte de réseau, onglet fermé pendant la requête, robot d'indexation) et pas
 * par notre code. On ne le remonte donc pas à Sentry.
 */
function isNetworkError(err: unknown): boolean {
  return (
    err instanceof TypeError &&
    NETWORK_ERROR_MESSAGES.some((message) => err.message.includes(message))
  );
}

/**
 * Intercepte fetch côté client pour gérer les erreurs globalement
 * (équivalent de handleFetch côté serveur)
 *
 * Cette fonction remplace window.fetch par une version qui intercepte
 * toutes les requêtes, y compris celles des fonctions load de SvelteKit.
 */
export function setupFetchInterceptor(): void {
  if (!browser || typeof window === "undefined") {
    return;
  }

  if ((window.fetch as any).__intercepted) {
    return;
  }

  const originalFetch = window.fetch;

  const interceptedFetch = async (
    input: string | URL | Request,
    init?: RequestInit
  ): Promise<Response> => {
    if (!isFirstPartyRequest(input)) {
      return originalFetch(input, init);
    }

    let response: Response;
    try {
      response = await originalFetch(input, init);
    } catch (err) {
      if (!isNetworkError(err)) {
        Sentry.captureException(err);
      }
      throw err;
    }

    if (response.status === 429) {
      Sentry.captureMessage(response.statusText);
      toast.push(RATE_LIMIT_MESSAGE);
    }

    return response;
  };

  window.fetch = interceptedFetch;

  (window.fetch as any).__intercepted = true;
}
