const config = {
  mode: "jit",
  purge: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    colors: {
      transparent: "transparent",
      current: "currentColor",
      gray: {
        "00": "#F5F5F5",
        "01": "#E0E0E0",
        "02": "#D5D5D5",
        "03": "#CCCCC",
        text: { DEFAULT: "#555555", alt: "#999999", alt2: "#777777" },
        dark: "#2E2E2E",
      },
      "france-blue": "#000091",
      white: "#FFFFFF",
      "marianne-red": "#E1000F",
      dora: {
        magenta: {
          brand: "#9C6FF4",
          hover: "#7B40F0",
          cta: "#5B12EB",
        },
      },
      magenta: {
        80: "#AF8EF3",
        60: "#C3AAF6",
        40: "#D7C6F9",
        20: "#EBE3FB",
        10: "#F5F0FD",
      },
      success: "#008941",
      error: "#E10600",
      information: { DEFAULT: "#0762C8", bg: "#DBF0FF", light: "#F0F8FF" },
    },
    fontFamily: {
      sans: ["Marianne"],
    },
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")],
};

module.exports = config;
