import { error } from "@sveltejs/kit";
import { browser } from "$app/environment";
import { API_URL, INTERNAL_API_URL } from "$lib/env";
import * as Sentry from "@sentry/sveltekit";

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
    // Déclenche l'affichage du message d'erreur du fichier +error.svelte racine
    error(429, response.statusText);
  }

  return response;
}
