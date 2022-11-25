import adapter from "@sveltejs/adapter-node";
import preprocess from "svelte-preprocess";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  // for more information about preprocessors
  preprocess: [
    preprocess({
      postcss: true,
    }),
  ],

  kit: {
    adapter: adapter({}),
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
    if (warning.code === "security-anchor-rel-noreferrer") return;

    // Désactivation des avertissements d'accessibilité, le temps de finir la migration Sveltekit
    // TODO: les corriger au lieu de les masquer
    if (warning.code === "a11y-click-events-have-key-events") return;
    if (warning.code === "a11y-label-has-associated-control") return;
    if (warning.code === "a11y-role-has-required-aria-props") return;

    defaultHandler(warning);
  },
};

export default config;
