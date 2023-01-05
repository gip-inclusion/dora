module.exports = {
  root: true,
  parser: "@typescript-eslint/parser",
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  plugins: ["svelte3", "@typescript-eslint"],
  ignorePatterns: ["*.cjs"],
  overrides: [{ files: ["*.svelte"], processor: "svelte3/svelte3" }],
  settings: {
    "svelte3/typescript": () => require("typescript"),
  },
  parserOptions: {
    sourceType: "module",
    ecmaVersion: 2020,
  },
  env: {
    browser: true,
    es2022: true,
    node: true,
  },
  globals: {
    tarteaucitron: "readonly",
  },
  rules: {
    eqeqeq: ["error", "smart"],
    "func-style": [
      "error",
      "declaration",
      {
        allowArrowFunctions: true,
      },
    ],
    "no-alert": "warn",
    "no-console": "off",
    "no-empty-function": "warn",
    "@typescript-eslint/no-empty-function": "warn",
    "no-return-assign": "error",
    "no-undef-init": "off",
    "no-undefined": "off",
    "no-underscore-dangle": "off",
    "no-unused-vars": ["off"],
    "@typescript-eslint/no-unused-vars": [
      "error",
      {
        argsIgnorePattern: "^_",
        varsIgnorePattern: "^_",
      },
    ],
    "@typescript-eslint/no-explicit-any": "off",
    "no-warning-comments": [
      "off",
      {
        location: "start",
        terms: ["todo", "hack", "xxx", "fixme"],
      },
    ],
    "node/no-missing-import": "off",
    "node/no-unpublished-import": "off",
    "node/no-unpublished-require": "off",
    "padding-line-between-statements": "off",
  },
};
