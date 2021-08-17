import * as Sentry from "@sentry/browser";

export async function handleError({ error, request }) {
  Sentry.captureException(error, { request });
}
