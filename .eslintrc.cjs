module.exports = {
  root: true,
  extends: ["eslint:recommended", "prettier"],
  plugins: ["svelte3"],
  overrides: [{ files: ["*.svelte"], processor: "svelte3/svelte3" }],
  parserOptions: {
    sourceType: "module",
    ecmaVersion: "latest",
  },
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  rules: {
    "no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
    "no-warning-comments": [
      "warn",
      {
        terms: ["todo", "hack", "xxx", "fixme"],
        location: "start",
      },
    ],
  },
};
