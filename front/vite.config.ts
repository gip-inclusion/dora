import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig, loadEnv } from "vite";
import { sentrySvelteKit } from "@sentry/sveltekit";
import { svelteTesting } from "@testing-library/svelte/vite";

export default defineConfig(({ mode }) => {
  // Charge les variables d'environnement des fichiers .env
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };
  return {
    plugins: [
      sentrySvelteKit({
        sourceMapsUploadOptions: {
          telemetry: false,
        },
      }),
      sveltekit(),
      svelteTesting(),
    ],

    build: {
      sourcemap: true,
    },
    server: {
      host: true,
    },
    test: {
      environment: "jsdom",
      globals: true,
      setupFiles: ["./vitest-setup.js"],
      includeSource: ["src/**/*.{js,ts,svelte}"],
      include: ["src/**/*.{test,spec}.{js,ts}"],
    },
  };
});
