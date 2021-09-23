// import * as Sentry from "@sentry/browser";

export function assert(condition, message) {
  if (!condition) {
    console.assert(message);
  }
  // Sentry.captureException(new Error(message));
}

export function logException(exc) {
  console.error(exc);
  // Sentry.captureException(exc);
}
export function log(message, ...args) {
  console.log(message);
  // Sentry.captureMessage(message, { extra: { ...args } });
}
