import * as Sentry from "@sentry/browser";

export function assert(condition, message) {
  if (!condition) {
    console.assert(message);
  }
  Sentry.captureException(new Error(message));
}

export function logException(exc, ...args) {
  console.error(exc);
  Sentry.captureException(exc, { extra: { ...args } });
}
export function log(message, ...args) {
  console.warning(message);
  Sentry.captureMessage(message, { extra: { ...args } });
}
