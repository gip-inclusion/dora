import * as v from "./utils";

export const addUserSchema = {
  email: {
    default: "",
    required: true,
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
  level: {
    default: "",
    required: true,
    rules: [
      v.isString(),
      (name, value, _data) => ({
        valid: value === "user" || value === "admin",
        msg: `Choix incorrect`,
      }),
    ],
  },
};

export const modifyUserSchema = {
  level: {
    default: "",
    required: true,
    rules: [
      v.isString(),
      (name, value, _data) => ({
        valid: value === "user" || value === "admin",
        msg: `Choix incorrect`,
      }),
    ],
  },
};
