import * as Sentry from "@sentry/sveltekit";
import { ENVIRONMENT, SENTRY_DSN } from "$lib/env";
import type { HandleClientError } from "@sveltejs/kit";

import { setupFetchInterceptor } from "$lib/utils/fetch-interceptor";
import { STALE_CHUNK_ERROR_MESSAGE } from "$lib/consts";

setupFetchInterceptor();

if (ENVIRONMENT !== "local") {
  Sentry.init({
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    tracesSampleRate: 0,
    tracePropagationTargets: [],
    ignoreErrors: [STALE_CHUNK_ERROR_MESSAGE],
  });
}

export const handleError: HandleClientError = Sentry.handleErrorWithSentry(
  ({ error }) => {
    // Quand un chunk JS ne peut plus être chargé (ex: après un déploiement qui
    // change les hash des fichiers), on force un rechargement complet de la page
    // pour que le navigateur récupère le nouvel HTML et les nouveaux chunks.
    if (
      error instanceof TypeError &&
      error.message.includes(STALE_CHUNK_ERROR_MESSAGE)
    ) {
      window.location.reload();
      return {};
    }

    const message =
      ENVIRONMENT === "local" && error instanceof Error
        ? error.message
        : "Erreur inattendue";

    return {
      message,
    };
  }
);
