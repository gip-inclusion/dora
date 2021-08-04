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
        "03": "#CCCCCC",
        text: { DEFAULT: "#555555", alt: "#999999", alt2: "#777777" },
        dark: "#2E2E2E",
        bg: "#F8F8F8",
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
    fontSize: {
      xs: ".75rem", // 12px
      sm: ".875rem", // 14px
      base: "1rem", // 16px
      lg: "1.0625rem", // 17px
      xl: "1.125rem", // 18px
      "2xl": "1.1875rem", // 19px
      "3xl": "1.25rem", // 20px
      "4xl": "1.3125rem", // 21px
      "5xl": "1.375rem", // 22px
      "6xl": "1.4375rem", // 23px
      "7xl": "1.5rem", // 24px
      "8xl": "1.625rem", // 26px
      "9xl": "1.75rem", // 28px
      "10xl": "1.875rem", // 30px
      "11xl": "2rem", // 32px
      "12xl": "2.375rem", // 38px
      "13xl": "2.8125rem", // 45px
    },
    lineHeight: {
      tight: "1.2",
      normal: "1.5",
    },
    screens: { md: "375px", lg: "768px", xl: "1200px" },
    spacing: {
      0: "0",
      "2p": "0.125rem", //2px
      "1/2": "0.25rem", // 4px
      "3/4": "0.375rem", // 6px
      1: "0.5rem", // 8px
      "5/4": "0.625rem", //10px
      "3/2": "0.75rem", // 12px
      2: "1rem", // 16px
      "5/2": "1.25rem", // 20px
      3: "1.5rem", // 24px
      4: "2rem", // 32px
      5: "2.5rem",
      6: "3rem",
      7: "3.5rem",
      8: "4rem",
      9: "4.5rem",
      10: "5rem",
      11: "5.5rem",
      12: "6rem",
      14: "7rem",
      17: "8.5rem",
      20: "10rem",
    },
    borderRadius: {
      none: "0",
      DEFAULT: "0.25rem",
      md: "0.5rem",
      lg: "1.5rem",
      full: "9999px",
    },
    boxShadow: {
      none: "none",
      xs: "0 1px 0 0 rgba(0, 0, 0, 0.05)",
      sm: "0 0 1px 0  rgba(0, 0, 0, 0.05), 0 2px 1px 0 rgba(0, 0, 0, 0.05)",
      md: "0 2px 10px 0 rgba(0, 0, 0, 0.1), 0 0 2px 0 rgba(0, 0, 0, 0.2)",
      l: "0 4px 20px 0 rgba(0, 0, 0, 0.15), 0 0 3px 0 rgba(0, 0, 0, 0.1)",
      xl: "0 0 4px rgba(0, 0, 0, 0.1), 0px 8px 40px rgba(0, 0, 0, 0.2);",
      inner: "inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)",
      focus: "0px 0px 0px 2px #FFFFFF, 0px 0px 0px 4px #0A76F6",
    },
  },
  plugins: [require("@tailwindcss/typography")],
};

module.exports = config;
