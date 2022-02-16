const preprocess = require("svelte-preprocess");

module.exports = {
  stories: [
    "../src/**/*.stories.mdx",
    "../src/**/*.stories.@(js|jsx|ts|tsx|svelte)",
  ],
  addons: ["@storybook/addon-essentials", "@storybook/addon-links"],
  framework: "@storybook/svelte",
  core: {
    builder: "storybook-builder-vite",
  },
  svelteOptions: {
    preprocess: [preprocess({ postcss: true, sourceMap: true })],
  },
};
