import type { Handle, HandleFetch, HandleServerError } from "@sveltejs/kit";
import { sequence } from "@sveltejs/kit/hooks";
import { error } from "@sveltejs/kit";

import * as Sentry from "@sentry/sveltekit";

import { RetryAfterRateLimiter } from "sveltekit-rate-limiter/server";

import { ENVIRONMENT, SENTRY_DSN } from "$lib/env";

import { MAX_REQUESTS_PER_MINUTE } from "$env/static/private";

const rateLimiter = new RetryAfterRateLimiter({
  IPUA: [Number(MAX_REQUESTS_PER_MINUTE) || 24, "m"],
});

if (ENVIRONMENT !== "local") {
  Sentry.init({
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    tracesSampleRate: 0,
    tracePropagationTargets: [],
  });
}

export const handleError: HandleServerError = Sentry.handleErrorWithSentry(
  ({ error: err }) => {
    const message =
      ENVIRONMENT === "local" && err instanceof Error
        ? err.message
        : "Erreur inattendue";

    return {
      message,
    };
  }
);

export const handle: Handle = sequence(
  Sentry.sentryHandle({ injectFetchProxyScript: false }),
  async ({ event, resolve }) => {
    const status = await rateLimiter.check(event);
    if (status.limited) {
      throw error(
        429,
        `Trop de requêtes. Réessayez après ${status.retryAfter} secondes.`
      );
    }

    const response = await resolve(event);

    if (ENVIRONMENT !== "production") {
      response.headers.set("X-Robots-Tag", "noindex");
    }
    response.headers.set("X-Frame-Options", "DENY");
    response.headers.set("X-XSS-Protection", "1; mode=block");
    response.headers.set("X-Content-Type-Options", "nosniff");
    response.headers.set("Referrer-Policy", "strict-origin");

    return response;
  }
);

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
  const headers = new Headers(request.headers);
  headers.set("X-Forwarded-For", event.getClientAddress());

  const modifiedRequest = new Request(request, {
    headers,
  });

  const response = await fetch(modifiedRequest);

  if (response.status === 429) {
    Sentry.captureMessage(response.statusText);
    // Erreur attendue 429 (rate limiting)
    // Déclenche l'affichage du message d'erreur du fichier +error.svelte racine
    error(429, response.statusText);
  }

  return response;
};
