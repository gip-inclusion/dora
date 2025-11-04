import * as Sentry from "@sentry/sveltekit";
import { ENVIRONMENT, SENTRY_DSN } from "$lib/env";
import type { HandleClientError } from "@sveltejs/kit";

import { setupFetchInterceptor } from "$lib/utils/fetch-interceptor";

setupFetchInterceptor();

if (ENVIRONMENT !== "local") {
  Sentry.init({
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    tracesSampleRate: 0,
    tracePropagationTargets: [],
  });
}

export const handleError: HandleClientError = Sentry.handleErrorWithSentry(
  ({ error }) => {
    const message =
      ENVIRONMENT === "local" && error instanceof Error
        ? error.message
        : "Erreur inattendue";

    return {
      message,
    };
  }
);
