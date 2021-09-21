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
    },
  };
}
