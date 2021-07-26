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
      server: {
        hmr: {
          protocol: "ws",
          port: 3001,
        },
      },
    },
    adapter: node({
      // default options are shown
      out: "build",
      precompress: false,
      env: {
        // host: 'HOST',
        // port: 'PORT'
      },
    }),
  },

  preprocess: [
    preprocess({
      postcss: true,
    }),
  ],
};

export default config;
// Workaround until SvelteKit uses Vite 2.3.8 (and it's confirmed to fix the Tailwind JIT problem)
const mode = process.env.NODE_ENV;
const dev = mode === "development";
process.env.TAILWIND_MODE = dev ? "watch" : "build";
