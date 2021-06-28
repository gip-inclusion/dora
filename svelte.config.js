/** @type {import('@sveltejs/kit').Config} */
import adapter from "@sveltejs/adapter-node";

const config = {
  kit: {
    // hydrate the <div id="svelte"> element in src/app.html
    target: "#svelte",
    vite: {
      server: {
        hmr: {
          protocol: "ws",
          port: 3001,
        },
      },
    },
    adapter: adapter({
      // default options are shown
      out: "build",
      precompress: false,
      env: {
        // host: 'HOST',
        // port: 'PORT'
      },
    }),
  },
};

export default config;
