import { ENVIRONMENT, SENTRY_DSN } from "$lib/env";
import * as Sentry from "@sentry/browser";
import type { HandleClientError } from "@sveltejs/kit";

if (ENVIRONMENT !== "local") {
  Sentry.init({
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    tracesSampleRate: 0,
  });
}

export const handleError: HandleClientError = ({ error, event }) => {
  Sentry.captureException(error, { event });

  const message = ENVIRONMENT === "local" ? error.message : "Erreur inattendue";

  return {
    message,
  };
};
