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
  staticDirs: ["../static"],
  svelteOptions: {
    preprocess: [preprocess({ postcss: true, sourceMap: true })],
  },

  async viteFinal(config, { configType }) {
    // déploiement dans un sous dossier sur github pages
    // github.com/storybookjs/storybook/discussions/17433
    // BASE_URL est défini dans `.github/workflows/storybook.yml`
    config.base = process.env.BASE_URL || config.base;

    return config;
  },
};
