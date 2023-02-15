import adapter from "@sveltejs/adapter-node";
import { vitePreprocess } from "@sveltejs/kit/vite";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),

  kit: {
    adapter: adapter({ precompress: true }),
    csp: {
      mode: "nonce",
      directives: {
        "base-uri": ["self"],
        "default-src": ["none"],
        "connect-src": [
          process.env?.VITE_API_URL,
          process.env?.VITE_ENVIRONMENT === "local" ? "ws:" : null,
          "https://*.sentry.incubateur.net",
          "https://api-adresse.data.gouv.fr/",
          "https://client.crisp.chat/static/",
          "https://plausible.io/api/event",
          "https://sentry.incubateur.net",
          "https://storage.crisp.chat/users/upload/",
          "wss://client.relay.crisp.chat/",
          "https://openmaptiles.geo.data.gouv.fr/",
          "https://openmaptiles.github.io/osm-bright-gl-style/",
        ].filter((source) => !!source),
        "script-src": [
          "self",
          "strict-dynamic",
          "unsafe-inline",
          "https://client.crisp.chat/",
          "https://metabase.dora.fabrique.social.gouv.fr/app/iframeResizer.js",
          "https://plausible.io/js/",
          "https://tally.so/widgets/embed.js",
        ],
        "worker-src": ["self", "blob:"],
        "child-src": [
          "https://aide.dora.fabrique.social.gouv.fr/",
          "https://metabase.dora.fabrique.social.gouv.fr",
          "https://plausible.io",
          "https://tally.so",
        ],
        "font-src": ["self", "https://client.crisp.chat/static/"],
        "img-src": ["self", "data:", "https://*.crisp.chat/"],
        "style-src": [
          "self",
          "https://client.crisp.chat/",
          "https://tally.so/widgets/embed.js",
          "unsafe-inline",
        ],
      },
    },
    env: {
      publicPrefix: "VITE_PUBLIC_",
    },
  },
  vitePlugin: {
    experimental: {
      inspector: {
        showToggleButton: "always",
        toggleButtonPos: "bottom-right",
      },
    },
  },
  onwarn(warning, defaultHandler) {
    if (warning.code === "security-anchor-rel-noreferrer") {
      return;
    }

    // Désactivation des avertissements d'accessibilité, le temps de finir la migration Sveltekit
    // TODO: les corriger au lieu de les masquer
    if (warning.code === "a11y-click-events-have-key-events") {
      return;
    }
    if (warning.code === "a11y-label-has-associated-control") {
      return;
    }
    if (warning.code === "a11y-role-has-required-aria-props") {
      return;
    }

    defaultHandler(warning);
  },
};

export default config;
