import preprocess from "svelte-preprocess";
/** @type {import('@sveltejs/kit').Config} */
import node from "@sveltejs/adapter-node";

const config = {
  kit: {
    // hydrate the <div id="svelte"> element in src/app.html
    target: "#svelte",
    vite: {
      optimizeDeps: {
        include: ["insane", "@sentry/node", "@sentry/browser"],
      },
      build: {
        sourcemap: true,
      },
    },
    adapter: node({
      // default options are shown
      out: "build",
      precompress: true,
    }),
  },

  preprocess: [
    preprocess({
      postcss: true,
    }),
  ],
};

export default config;
