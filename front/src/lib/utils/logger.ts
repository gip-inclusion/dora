import * as Sentry from "@sentry/sveltekit";

export function logException(exc: unknown, ...args: unknown[]): void {
  Sentry.captureException(exc, { extra: { ...args } });
  // eslint-disable-next-line no-console
  console.error(exc, ...args);
}

export function log(message: string, ...args: unknown[]): void {
  Sentry.captureMessage(message, { extra: { ...args } });
  // eslint-disable-next-line no-console
  console.warn(message, ...args);
}
