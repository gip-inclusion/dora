import { browser } from "$app/environment";
import { API_URL, INTERNAL_API_URL } from "$lib/env";
import * as Sentry from "@sentry/sveltekit";
import { toast } from "@zerodevx/svelte-toast";

export function getApiURL() {
  if (browser || !INTERNAL_API_URL) {
    return API_URL;
  }
  return INTERNAL_API_URL;
}

export const defaultAcceptHeader = "application/json; version=1.0";

export async function customFetch(
  input: string | URL | globalThis.Request,
  init?: RequestInit
): Promise<Response> {
  const response: Response = await fetch(input, init);

  if (response.status === 429) {
    Sentry.captureMessage(response.statusText);
    // Erreur attendue 429 (rate limiting)
    // Affichage d'un message d'erreur dans un toast
    toast.push("Trop de requêtes. Réessayez après 1 minute.");
  }

  return response;
}
