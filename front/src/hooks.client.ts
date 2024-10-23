import * as Sentry from "@sentry/sveltekit";
import { ENVIRONMENT, SENTRY_DSN } from "$lib/env";
import type { HandleClientError } from "@sveltejs/kit";

if (ENVIRONMENT !== "local") {
  Sentry.init({
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    tracesSampleRate: 0,
    tracePropagationTargets: [],
  });
}

export const handleError: HandleClientError = Sentry.handleErrorWithSentry(
  ({ error, _event }) => {
    const message =
      ENVIRONMENT === "local" ? error.message : "Erreur inattendue";

    return {
      message,
    };
  }
);
