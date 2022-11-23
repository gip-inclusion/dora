import { dev } from "$app/environment";

import { API_URL, CANONICAL_URL, ENVIRONMENT } from "$lib/env";
import * as Sentry from "@sentry/browser";

export async function handleError({ error, event }) {
  Sentry.captureException(error, { event });
}

export async function handle({ event, resolve }) {
  const response = await resolve(event);

  const connectSrc = `connect-src ${API_URL} ${
    dev ? "ws:" : ""
  } https://api-adresse.data.gouv.fr/ https://plausible.io/api/event https://sentry.incubateur.net https://*.sentry.incubateur.net https://client.crisp.chat/static/ wss://client.relay.crisp.chat/ https://storage.crisp.chat/users/upload/`;
  const scriptSrc = `script-src 'self' 'unsafe-inline' https://metabase.dora.fabrique.social.gouv.fr/app/iframeResizer.js https://plausible.io/js/ https://tally.so/widgets/embed.js https://client.crisp.chat/`;
  const frameSrc = `frame-src https://metabase.dora.fabrique.social.gouv.fr https://plausible.io https://tally.so https://aide.dora.fabrique.social.gouv.fr/`;
  const fontSrc = `font-src 'self' https://client.crisp.chat/static/`;
  const imgSrc = `img-src 'self' data: https://*.crisp.chat/`;
  const styleSrc = `style-src 'self' 'unsafe-inline' https://client.crisp.chat/`;

  if (ENVIRONMENT !== "production") {
    response.headers.set("X-Robots-Tag", "noindex");
  }
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-XSS-Protection", "1; mode=block");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set(
    "Content-Security-Policy",
    `default-src 'none';  ${connectSrc}; ${scriptSrc}; ${fontSrc}; ${imgSrc}; ${styleSrc}; ${frameSrc}`
  );

  if (response.headers.get("content-type")?.startsWith("text/html")) {
    const body = await response.text();
    return new Response(
      body.replace("%plausible-domain%", CANONICAL_URL.split("//")[1]),
      response
    );
  }
  return response;
}
