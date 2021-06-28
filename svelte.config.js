/** @type {import('@sveltejs/kit').Config} */
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
  },
};

export default config;
