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
    // BASE_URL est définie dans `.github/workflows/storybook.yml`
    const baseUrl = process.env.BASE_URL;

    if (baseUrl) {
      config.base = `${baseUrl}/`;
    }

    // bug en production :
    // `Uncaught Error: Singleton client API not yet initialized, cannot call addParameters`
    // github.com/storybookjs/storybook/issues/10887#issuecomment-901109891
    config.resolve.dedupe = ["@storybook/client-api"];

    return config;
  },
};
