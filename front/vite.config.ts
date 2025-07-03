import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig, loadEnv } from "vite";
import { sentrySvelteKit } from "@sentry/sveltekit";
import tailwindcss from "@tailwindcss/vite";

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
      tailwindcss(),
    ],

    build: {
      sourcemap: true,
      target: "esnext",
      minify: "esbuild",
    },
    server: {
      host: true,
      hmr: {
        overlay: true,
      },
    },
    optimizeDeps: {
      include: ["svelte"],
    },
    test: {
      include: ["src/**/*.{test,spec}.{js,ts}"],
    },
  };
});
