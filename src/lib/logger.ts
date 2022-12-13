import * as Sentry from "@sentry/svelte";

export function logException(exc, ...args) {
  Sentry.captureException(exc, { extra: { ...args } });
  // eslint-disable-next-line no-console
  console.error(exc, ...args);
}

export function log(message, ...args) {
  Sentry.captureMessage(message, { extra: { ...args } });
  // eslint-disable-next-line no-console
  console.warn(message, ...args);
}
