const tailwindcss = require("tailwindcss");
const autoprefixer = require("autoprefixer");
const cssnano = require("cssnano");
const url = require("postcss-url");

const dev = process.env.NODE_ENV === "development";
const baseUrl = process.env.BASE_URL;

const config = {
  plugins: [
    // Some plugins, like postcss-nested, need to run before Tailwind,
    tailwindcss(),
    // But others, like autoprefixer, need to run after,
    autoprefixer(),
    !dev && cssnano({ preset: "default" }),
    // déploiement du design system dans un sous dossier sur github pages
    // BASE_URL est définie dans `.github/workflows/storybook.yml`
    baseUrl && url({ url: (asset) => `${baseUrl}${asset.url}` }),
  ],
};

module.exports = config;
