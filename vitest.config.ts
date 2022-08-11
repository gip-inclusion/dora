import { defineConfig } from "vitest/config";
import { sveltekit } from "@sveltejs/kit/vite";

export default defineConfig({
  test: {
    deps: {
      inline: ["@sentry/utils", "@sentry/hub", "@sentry/browser"],
    },
  },
  plugins: [sveltekit()],
});
