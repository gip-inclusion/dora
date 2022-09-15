import { dev } from "$app/env";

import { API_URL, ENVIRONMENT } from "$lib/env";
import * as Sentry from "@sentry/browser";

export async function handleError({ error, event }) {
  Sentry.captureException(error, { event });
}

// Pages sur lesquelles ont ne veut pas de SSR…
const noSsrPaths = [
  // pour raison de performance, les requêtes étant lourdes, et on ne tient pas forcément
  // à ce qu'elles soient indexées
  "/recherche",

  // pages authentifiée ou effectuant des actions particulières avec le token,
  // que le SSR pourrait invalider
  "/auth",

  // pages authentifiées sur lesquelles la première requête non authentifiée n'a pas de sens
  "/services/creer",
  "/structures/creer",
  "/modeles/creer",
  "/mon-compte",
  "/admin",

  // page de débug où on veut tester hors SSR
  "/sentry-debug-client",
];

export async function handle({ event, resolve }) {
  let ssr = !noSsrPaths.some((s) => event.url.pathname.startsWith(s));

  // No SSR for testing => we can't intercept request server side
  if (ENVIRONMENT === "testing") ssr = false;

  const response = await resolve(event, { ssr });

  const connectSrc = `connect-src ${API_URL} ${
    dev ? "ws:" : ""
  } https://api-adresse.data.gouv.fr/ https://plausible.io/api/event https://sentry.incubateur.net https://*.sentry.incubateur.net https://client.crisp.chat/static/ wss://client.relay.crisp.chat/ https://storage.crisp.chat/users/upload/`;
  const scriptSrc = `script-src 'self' 'unsafe-inline' https://metabase.dora.fabrique.social.gouv.fr/app/iframeResizer.js https://plausible.io/js/ https://tally.so/widgets/embed.js https://client.crisp.chat/`;
  const frameSrc = `frame-src https://metabase.dora.fabrique.social.gouv.fr https://plausible.io https://tally.so https://aide.dora.fabrique.social.gouv.fr/`;
  const fontSrc = `font-src 'self' https://client.crisp.chat/static/`;
  const imgSrc = `img-src 'self' data: https://*.crisp.chat/`;
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
