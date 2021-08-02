import preprocess from "svelte-preprocess";
/** @type {import('@sveltejs/kit').Config} */
import node from "@sveltejs/adapter-node";

const config = {
  kit: {
    // hydrate the <div id="svelte"> element in src/app.html
    target: "#svelte",
    vite: {
      optimizeDeps: {
        include: ["insane"],
      },
    },
    adapter: node({
      // default options are shown
      out: "build",
      precompress: false,
    }),
  },

  preprocess: [
    preprocess({
      postcss: true,
    }),
  ],
};

export default config;
