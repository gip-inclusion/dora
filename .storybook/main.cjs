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
  // lorsqu'on génère storybook pour l'afficher sur github pages (dans un sous-dossier),
  // on veut modifier l'url des import des fichier @font-face
  previewHead: (head) => {
    const baseUrl = process.env.BASE_URL || "";

    return `${head}
<style>
  @font-face {
    font-display: swap;
    font-family: "Marianne";
    font-style: normal;
    font-weight: normal;
    src: url("${baseUrl}/fonts/Marianne/Marianne-Regular.woff2") format("woff2"),
         url("${baseUrl}/fonts/Marianne/Marianne-Regular.woff") format("woff");
  }

  @font-face {
    font-display: swap;
    font-family: "Marianne";
    font-style: normal;
    font-weight: bold;
    src: url("${baseUrl}/fonts/Marianne/Marianne-Bold.woff2") format("woff2"),
        url("${baseUrl}/fonts/Marianne/Marianne-Bold.woff") format("woff");
  }

  @font-face {
    font-display: swap;
    font-family: "Marianne";
    font-style: italic;
    font-weight: normal;
    src: url("${baseUrl}/fonts/Marianne/Marianne-Regular_Italic.woff2") format("woff2"),
        url("${baseUrl}/fonts/Marianne/Marianne-Regular_Italic.woff") format("woff");
  }

  @font-face {
    font-display: swap;
    font-family: "Marianne";
    font-style: italic;
    font-weight: bold;
    src: url("${baseUrl}/fonts/Marianne/Marianne-Bold_Italic.woff2") format("woff2"),
        url("${baseUrl}/fonts/Marianne/Marianne-Bold_Italic.woff") format("woff");
  }
</style>
  `;
  },
};
