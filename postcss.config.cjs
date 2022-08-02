const tailwindcss = require("tailwindcss");
const autoprefixer = require("autoprefixer");
const cssnano = require("cssnano");

const dev = process.env.NODE_ENV === "development";

const config = {
  plugins: [
    // Some plugins, like postcss-nested, need to run before Tailwind,
    tailwindcss(),
    // But others, like autoprefixer, need to run after,
    autoprefixer(),
    !dev && cssnano({ preset: "default" }),
  ],
};

module.exports = config;
