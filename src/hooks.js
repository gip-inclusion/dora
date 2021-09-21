import { API_URL } from "$lib/env";
// import * as Sentry from "@sentry/browser";

// export async function handleError({ error, request }) {
//   Sentry.captureException(error, { request });
// }

export async function handle({ request, resolve }) {
  const response = await resolve(request);

  return {
    ...response,
    headers: {
      ...response.headers,
      "X-Frame-Options": "DENY",
      "X-XSS-Protection": "1; mode=block",
      "X-Content-Type-Options": "nosniff",
      "Content-Security-Policy": `default-src 'none'; connect-src ${API_URL} https://api-adresse.data.gouv.fr/search/ https://plausible.io/api/event; font-src 'self'; img-src 'self' data:; script-src 'self' 'unsafe-inline' https://plausible.io/js/plausible.js; style-src 'self' 'unsafe-inline'`,
    },
  };
}
