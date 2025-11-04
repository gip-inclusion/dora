import { browser } from "$app/environment";
import * as Sentry from "@sentry/sveltekit";
import { toast } from "@zerodevx/svelte-toast";

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
    const response = await originalFetch(input, init);

    if (response.status === 429) {
      Sentry.captureMessage(response.statusText);
      toast.push(
        "Vous avez effectué trop de requêtes. Veuillez patienter une minute avant de réessayer."
      );
    }

    return response;
  };

  window.fetch = interceptedFetch;

  (window.fetch as any).__intercepted = true;
}
