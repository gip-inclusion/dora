import { dev } from "$app/env";

import { API_URL } from "$lib/env";
import * as Sentry from "@sentry/browser";

export async function handleError({ error, request }) {
  Sentry.captureException(error, { request });
}

export async function handle({ request, resolve }) {
  const response = await resolve(request);

  const connectSrc = `connect-src ${API_URL} ${
    dev ? "ws:" : ""
  } https://api-adresse.data.gouv.fr/search/ https://plausible.io/api/event https://*.sentry.io`;
  const scriptSrc = `script-src 'self' 'unsafe-inline' https://plausible.io/js/plausible.js https://static.hotjar.com https://script.hotjar.com `;
  const frameSrc = `frame-src https://vars.hotjar.com/`;
  return {
    ...response,
    headers: {
      ...response.headers,
      "X-Frame-Options": "DENY",
      "X-XSS-Protection": "1; mode=block",
      "X-Content-Type-Options": "nosniff",
      "Content-Security-Policy": `default-src 'none';  ${connectSrc}; ${scriptSrc}; font-src 'self'; img-src 'self' data:;  style-src 'self' 'unsafe-inline'; ${frameSrc}`,
    },
  };
}
