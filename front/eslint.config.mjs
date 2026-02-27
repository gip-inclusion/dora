import typescriptEslint from "@typescript-eslint/eslint-plugin";
import globals from "globals";
import tsParser from "@typescript-eslint/parser";
import parser from "svelte-eslint-parser";
import path from "node:path";
import { fileURLToPath } from "node:url";
import eslintJs from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";
import sveltePlugin from "eslint-plugin-svelte";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: eslintJs.configs.recommended,
  allConfig: eslintJs.configs.all,
});

export default [
  {
    ignores: [
      "**/*.cjs",
      "**/.DS_Store",
      "**/node_modules",
      "build",
      "static",
      ".svelte-kit",
      "package",
      "**/.env",
      "**/.env.*",
      "!**/.env.example",
      "**/pnpm-lock.yaml",
      "**/package-lock.json",
      "**/yarn.lock",
      "**/.history",
    ],
  },
  ...compat.extends(
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ),
  {
    plugins: {
      "@typescript-eslint": typescriptEslint,
      svelte: sveltePlugin,
    },

    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },

      parser: tsParser,
      ecmaVersion: 2020,
      sourceType: "module",

      parserOptions: {
        extraFileExtensions: [".svelte"],
      },
    },

    rules: {
      ...sveltePlugin.configs.recommended.rules,
      "array-callback-return": "error",
      "block-scoped-var": "error",
      camelcase: "error",
      "consistent-return": "error",
      "consistent-this": "error",
      curly: "error",
      "default-case": "error",
      "default-case-last": "error",
      "default-param-last": ["error"],
      "dot-notation": "error",
      eqeqeq: ["error", "smart"],

      "id-length": [
        "error",
        {
          min: 3,
          exceptions: ["i", "a", "b", "v", "x", "y", "id", "ok", "to"],
        },
      ],

      "func-style": [
        "error",
        "declaration",
        {
          allowArrowFunctions: true,
        },
      ],

      "guard-for-in": "error",
      "no-alert": "warn",
      "no-await-in-loop": "error",
      "no-console": "warn",
      "no-constant-binary-expression": "error",
      "no-empty-function": "warn",
      "no-eval": "error",

      "no-extra-boolean-cast": [
        "error",
        {
          enforceForLogicalOperands: true,
        },
      ],

      "no-implicit-coercion": [
        2,
        {
          allow: ["!!"],
        },
      ],

      "no-implied-eval": "error",
      "no-irregular-whitespace": "off",
      "no-mixed-operators": "error",
      "no-nested-ternary": "error",
      "no-return-assign": "error",
      "no-return-await": "error",
      "no-shadow": "error",
      "no-unneeded-ternary": "error",
      "no-use-before-define": "error",
      "no-var": "error",

      "no-warning-comments": [
        "warn",
        {
          location: "start",
          terms: ["todo", "hack", "xxx", "fixme"],
        },
      ],

      "prefer-const": "off",
      "svelte/prefer-const": "off",
      "require-await": "error",
      "svelte/no-at-html-tags": "warn",
      "svelte/valid-compile": "warn",
      "@typescript-eslint/no-empty-function": "warn",

      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
        },
      ],

      "@typescript-eslint/no-explicit-any": "off",
    },
  },
  {
    files: ["**/*.svelte"],

    languageOptions: {
      parser: parser,
      ecmaVersion: 5,
      sourceType: "script",

      parserOptions: {
        parser: "@typescript-eslint/parser",
      },
    },

    rules: {
      "@typescript-eslint/no-unused-expressions": "off",
    },
  },
];
