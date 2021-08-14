import * as Sentry from "@sentry/browser";

export async function handleError({ error, request }) {
  console.log("*Capturing exception*", error, request);
  Sentry.captureException(error, { request });
}
