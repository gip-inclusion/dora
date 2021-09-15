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
    rules: [v.isString(), v.minStrLength(8)],
  },
};

export const pwChangeSchema = {
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

export const passwordLostSchema = {
  email: {
    default: "",
    required: true,
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
};
