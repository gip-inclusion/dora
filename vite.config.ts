import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  // Charge les variables d'environnement des fichiers .env
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };
  return {
    plugins: [sveltekit()],

    build: {
      sourcemap: true,
    },

    test: {
      include: ["src/**/*.{test,spec}.{js,ts}"],
    },
  };
});
