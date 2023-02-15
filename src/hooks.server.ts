import { ENVIRONMENT, SENTRY_DSN } from "$lib/env";
import * as Sentry from "@sentry/svelte";
import type { Handle, HandleServerError } from "@sveltejs/kit";

if (ENVIRONMENT !== "local") {
  Sentry.init({
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    tracesSampleRate: 0,
  });
}

export const handleError: HandleServerError = ({ error, event }) => {
  Sentry.captureException(error, { event });

  return {
    message: "Erreur inattendue",
  };
};

export const handle: Handle = async ({ event, resolve }) => {
  const response = await resolve(event);

  if (ENVIRONMENT !== "production") {
    response.headers.set("X-Robots-Tag", "noindex");
  }
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-XSS-Protection", "1; mode=block");
  response.headers.set("X-Content-Type-Options", "nosniff");

  return response;
};
