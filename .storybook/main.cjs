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
    // nécessaire pour le déploiement dans un sous dossier sur github pages
    // github.com/storybookjs/storybook/discussions/17433
    config.base = process.env.BASE_URL || config.base;

    // return the customized config
    return config;
  },
};
