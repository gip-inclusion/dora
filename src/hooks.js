import { dev } from "$app/env";

import { API_URL } from "$lib/env";
import * as Sentry from "@sentry/browser";

export async function handleError({ error, event }) {
  Sentry.captureException(error, { event });
}

// /auth utilise un token qui est invalidé sur le serveur après le premier appel.
// on ne veut donc pas qu'il soit requêté par le ssr puis par le le client
// on devrait pouvoir utiliser la function `fetch` disponible en paramètre de la function load.
const noSsrPaths = [
  "/recherche",
  "/auth",
  "/sentry-debug-client",
  "/services/creer",
  "/structures/creer",
  "/mon-compte",
];

export async function handle({ event, resolve }) {
  const ssr = !noSsrPaths.some((s) => event.url.pathname.startsWith(s));
  const response = await resolve(event, { ssr });

  // https://help.hotjar.com/hc/en-us/aFrticles/115011640307-Content-Security-Policies

  const connectSrc = `connect-src ${API_URL} ${
    dev ? "ws:" : ""
  } https://api-adresse.data.gouv.fr/ https://plausible.io/api/event https://*.sentry.io http://*.hotjar.com:* https://*.hotjar.com:* http://*.hotjar.io https://*.hotjar.io wss://*.hotjar.com  https://client.crisp.chat/static/ wss://client.relay.crisp.chat/ https://storage.crisp.chat/users/upload/`;
  const scriptSrc = `script-src 'self' 'unsafe-inline' https://metabase.dora.fabrique.social.gouv.fr/app/iframeResizer.js https://plausible.io/js/ https://static.hotjar.com https://script.hotjar.com http://*.hotjar.com https://*.hotjar.com http://*.hotjar.io https://*.hotjar.io https://client.crisp.chat/`;
  const frameSrc = `frame-src http://metabase.dora.fabrique.social.gouv.fr https://*.hotjar.com http://*.hotjar.io https://*.hotjar.io https://plausible.io`;
  const fontSrc = `font-src 'self' http://*.hotjar.com https://*.hotjar.com http://*.hotjar.io https://*.hotjar.io https://client.crisp.chat/static/`;
  const imgSrc = `img-src 'self' data: http://*.hotjar.com https://*.hotjar.com http://*.hotjar.io https://*.hotjar.io https://*.crisp.chat/`;
  const styleSrc = `style-src 'self' 'unsafe-inline' https://client.crisp.chat/`;

  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-XSS-Protection", "1; mode=block");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set(
    "Content-Security-Policy",
    `default-src 'none';  ${connectSrc}; ${scriptSrc}; ${fontSrc}; ${imgSrc}; ${styleSrc}; ${frameSrc}`
  );

  return response;
}
