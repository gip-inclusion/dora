import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig, loadEnv } from "vite";
import { sentrySvelteKit } from "@sentry/sveltekit/vite";
import tailwindcss from "@tailwindcss/vite";
import adapter from "@sveltejs/adapter-node";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

export default defineConfig(({ mode }) => {
  // Charge les variables d'environnement des fichiers .env
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };
  return {
    plugins: [
      sentrySvelteKit({
        telemetry: false,
      }),
      sveltekit({
        adapter: adapter({ precompress: true }),
        preprocess: vitePreprocess(),
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
              "https://data.geopf.fr/",
              "https://openmaptiles.data.gouv.fr",
              "https://openmaptiles.geo.data.gouv.fr/",
              "https://openmaptiles.github.io/osm-bright-gl-style/",
              "https://matomo.inclusion.beta.gouv.fr",
              "https://matomo.inclusion.gouv.fr",
              "https://api.collectivite.fr",
            ].filter((source) => !!source),
            "script-src": [
              "self",
              "unsafe-inline",
              "https://tally.so/widgets/embed.js",
              "https://matomo.inclusion.beta.gouv.fr",
              "https://matomo.inclusion.gouv.fr",
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
              "https://tally.so",
              "https://tube.numerique.gouv.fr",
            ],
            "img-src": ["self", "data:"],
            "style-src": [
              "self",
              "https://tally.so/widgets/embed.js",
              "unsafe-inline",
            ],
          },
        },
        inspector: {
          showToggleButton: "always",
          toggleButtonPos: "bottom-right",
        },
        onwarn(warning, defaultHandler) {
          // Désactivation des avertissements d'accessibilité, le temps de finir la migration Sveltekit
          // TODO: les corriger au lieu de les masquer
          const ignoredA11yWarnings = [
            "a11y_no_noninteractive_element_interactions",
          ];
          if (ignoredA11yWarnings.includes(warning.code)) {
            return;
          }

          // Le RGAA impose l'utilisation de ces `role`
          // et ces avertissements n'ont donc pas lieu d'être
          if (warning.code === "a11y_no_redundant_roles") {
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
      }),
      tailwindcss(),
    ],

    build: {
      sourcemap: true,
      target: "esnext",
    },
    server: {
      host: true,
      hmr: {
        overlay: true,
      },
    },
    resolve: {
      conditions: ["svelte", "browser", "module"],
    },
    optimizeDeps: {
      include: ["svelte"],
    },
    test: {
      include: ["src/**/*.{test,spec}.{js,ts}"],
    },
  };
});
