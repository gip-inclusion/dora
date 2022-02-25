import { ENVIRONMENT } from "$lib/env";
import * as v from "./utils";

export const loginSchema = {
  email: {
    default: "",
    required: true,
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
  password: {
    default: "",
    required: true,
    rules: [v.isString(), v.minStrLength(9)],
  },
};

export const passwordChangeSchema = {
  currentPassword: {
    default: "",
    required: true,
    rules: [v.isString(), v.minStrLength(9)],
  },
  newPassword1: {
    default: "",
    required: true,
    rules: [v.isString(), v.minStrLength(9)],
  },
  newPassword2: {
    default: "",
    required: true,
    rules: [
      v.isString(),
      v.minStrLength(9),
      (name, value, data) => ({
        valid: value === data.newPassword1,
        msg: `Les mots de passe ne sont pas identiques`,
      }),
    ],
  },
};

export const passwordLostSchema = {
  password1: {
    default: "",
    required: true,
    rules: [v.isString(), v.minStrLength(9)],
  },
  password2: {
    default: "",
    required: true,
    rules: [
      v.isString(),
      v.minStrLength(9),
      (name, value, data) => ({
        valid: value === data.password1,
        msg: `Les mots de passe ne sont pas identiques`,
      }),
    ],
  },
};

export const currentEmailSchema = {
  email: {
    default: "",
    required: true,
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
};

export const accountSchema = {
  firstName: {
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  lastName: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  email: {
    default: "",
    required: true,
    rules: [
      v.isEmail(),
      v.maxStrLength(255),

      (name, value, data) => ({
        valid: data.isPoleEmploi
          ? value.endsWith("@pole-emploi.fr") ||
            value.endsWith("@pole-emploi.net") ||
            (value.endsWith("@dora.beta.gouv.fr") &&
              ENVIRONMENT !== "production")
          : true,
        msg: `Merci de renseigner une adresse valide (@pole-emploi.fr ou @pole-emploi.net)`,
      }),
    ],
    post: [v.lower, v.trim],
  },
  password: {
    default: "",
    required: true,
    rules: [v.isString(), v.minStrLength(9)],
  },
  password2: {
    default: "",
    required: true,
    rules: [
      v.isString(),
      v.minStrLength(9),
      (name, value, data) => ({
        valid: value === data.password,
        msg: `Les mots de passe ne sont pas identiques`,
      }),
    ],
  },
  siret: {
    default: "",
    required: true,
    rules: [v.isString()],
  },
  newsletter: {
    default: false,
    required: true,
    rules: [v.isBool()],
  },
  isPoleEmploi: {
    default: false,
    required: true,
    rules: [v.isBool()],
  },
};

export const safirSearchSchema = {
  safirCode: {
    default: "",
    required: true,
    rules: [v.isString(), v.isSafir()],
    post: [v.trim],
  },
};

export const userProfileSchema = {
  firstName: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  lastName: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  email: {
    default: "",
    required: true,
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
  phoneNumber: {
    default: "",
    required: true,
    pre: [v.removeAllSpaces],
    rules: [v.isPhone()],
  },
  newsletter: {
    default: false,
    rules: [v.isBool()],
  },
};
