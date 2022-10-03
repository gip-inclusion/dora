import * as v from "./utils";

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
    pre: [v.removeAllNonDigits],
    rules: [v.isPhone()],
  },
  newsletter: {
    default: false,
    rules: [v.isBool()],
  },
};
