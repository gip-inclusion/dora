import { sequence } from "@sveltejs/kit/hooks";
import * as Sentry from "@sentry/sveltekit";
import { ENVIRONMENT, SENTRY_DSN } from "$lib/env";
import type { Handle, HandleServerError } from "@sveltejs/kit";

if (ENVIRONMENT !== "local") {
  Sentry.init({
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    tracesSampleRate: 0,
    tracePropagationTargets: [],
  });
}

export const handleError: HandleServerError = Sentry.handleErrorWithSentry(
  ({ error, _event }) => {
    const message =
      ENVIRONMENT === "local" ? error.message : "Erreur inattendue";

    return {
      message,
    };
  }
);

export const handle: Handle = sequence(
  Sentry.sentryHandle(),
  async ({ event, resolve }) => {
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
