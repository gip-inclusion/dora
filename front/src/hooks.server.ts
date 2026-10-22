import { error } from "@sveltejs/kit";
import { sequence } from "@sveltejs/kit/hooks";
import type {
  Handle,
  HandleFetch,
  HandleServerError,
} from "@sveltejs/kit/hooks";

import * as Sentry from "@sentry/sveltekit";

import { RetryAfterRateLimiter } from "sveltekit-rate-limiter/server";

import { ENVIRONMENT, SENTRY_DSN } from "#lib/env.js";
import { SENTRY_DATA_COLLECTION } from "#lib/sentry.js";
import { UNEXPECTED_ERROR_MESSAGE } from "#lib/consts.js";
import { handleInboundNexusAutoLogin } from "#lib/utils/nexus.js";
import { isApiRequest, setClientIpHeaders } from "#lib/server/client-ip.js";

import { MAX_REQUESTS_PER_MINUTE } from "$app/env/private";
import { TOKEN_KEY } from "#lib/utils/auth.js";

const rateLimiter = new RetryAfterRateLimiter({
  IPUA: [MAX_REQUESTS_PER_MINUTE, "m"],
});

if (ENVIRONMENT !== "local") {
  Sentry.init({
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    tracesSampleRate: 0,
    tracePropagationTargets: [],
    dataCollection: SENTRY_DATA_COLLECTION,
  });
}

export const handleError: HandleServerError = Sentry.handleErrorWithSentry(
  ({ error: err }) => {
    const message =
      ENVIRONMENT === "local" && err instanceof Error
        ? err.message
        : UNEXPECTED_ERROR_MESSAGE;

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

    const token = event.cookies.get(TOKEN_KEY);
    await handleInboundNexusAutoLogin(event.url, token);

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
  // Le secret partagé ne doit être envoyé qu'au back
  if (isApiRequest(request.url)) {
    const headers = new Headers(request.headers);
    setClientIpHeaders(headers, event.getClientAddress());
    request = new Request(request, { headers });
  }

  const response = await fetch(request);

  if (response.status === 429) {
    Sentry.captureMessage(response.statusText);
    // Erreur attendue 429 (rate limiting)
    // Déclenche l'affichage du message d'erreur du fichier +error.svelte racine
    error(429, response.statusText);
  }

  return response;
};
