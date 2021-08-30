import * as v from "./utils";

export default {
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
    post: [v.trim],
  },
};
