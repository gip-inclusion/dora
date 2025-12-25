import adapter from "@sveltejs/adapter-node";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

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
          "self",
          "data:",
          process.env?.VITE_API_URL,
          process.env?.VITE_ENVIRONMENT === "local" ? "ws:" : null,
          "https://*.sentry.io",
          "https://api-adresse.data.gouv.fr/",
          "https://openmaptiles.data.gouv.fr",
          "https://openmaptiles.geo.data.gouv.fr/",
          "https://openmaptiles.github.io/osm-bright-gl-style/",
          "https://matomo.inclusion.beta.gouv.fr",
          "https://api.collectivite.fr",
          "https://cse.google.com",
        ].filter((source) => !!source),
        "script-src": [
          "self",
          "unsafe-inline",
          "https://tally.so/widgets/embed.js",
          "https://matomo.inclusion.beta.gouv.fr",
          "https://cse.google.com",
          "https://www.google.com",
          "http://clients1.google.com",
          "http://cse.google.com/adsense/search/async-ads.js",
          "unsafe-eval",
        ],
        "worker-src": ["self", "blob:"],
        "child-src": [
          "https://aide.dora.inclusion.gouv.fr/",
          "https://metabase.dora.inclusion.gouv.fr",
          "https://tally.so",
          "https://tube.numerique.gouv.fr",
        ],
        "font-src": ["self"],
        "frame-src": [
          "self",
          "https://metabase.dora.inclusion.gouv.fr",
          "https://cse.google.com",
          "https://syndicatedsearch.goog",
          "https://tally.so",
          "https://tube.numerique.gouv.fr",
        ],
        "img-src": [
          "self",
          "data:",
          "https://www.google.com",
          "http://clients1.google.com",
          "https://ssl.gstatic.com",
          "https://encrypted-tbn0.gstatic.com",
        ],
        "style-src": [
          "self",
          "https://tally.so/widgets/embed.js",
          "unsafe-inline",
          "https://www.google.com",
        ],
      },
    },
    env: {
      publicPrefix: "VITE_PUBLIC_",
    },
  },
  vitePlugin: {
    inspector: {
      showToggleButton: "always",
      toggleButtonPos: "bottom-right",
    },
  },
  onwarn(warning, defaultHandler) {
    if (warning.code === "security-anchor-rel-noreferrer") {
      return;
    }

    // Désactivation des avertissements d'accessibilité, le temps de finir la migration Sveltekit
    // TODO: les corriger au lieu de les masquer
    const ignoredA11yWarnings = ["a11y-no-noninteractive-element-interactions"];
    if (ignoredA11yWarnings.includes(warning.code)) {
      return;
    }

    // Le RGAA impose l'utilisation de ces `role`
    // et ces avertissements n'ont donc pas lieu d'être
    if (warning.code === "a11y-no-redundant-roles") {
      if (
        warning.message.includes("Redundant role 'main'") ||
        warning.message.includes("Redundant role 'banner'") ||
        warning.message.includes("Redundant role 'contentinfo'")
      ) {
        return;
      }
    }

    defaultHandler(warning);
  },
};

export default config;
