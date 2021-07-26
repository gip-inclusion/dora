const colors = require("tailwindcss/colors");

const config = {
  mode: "jit",
  purge: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    extend: {
      colors: {
        "blue-dora": "#2B5787",
        action: "#000638",
        accent: "#6A20AE",
        back1: "#DEDBEE",
        back2: "#F1F5F6",
      },
    },
    fontFamily: {
      sans: ["Marianne"],
    },
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")],
};

module.exports = config;
