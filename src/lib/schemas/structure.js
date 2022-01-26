import * as v from "./utils";

export default {
  siret: {
    default: "",
    required: true,
    rules: [v.isSiret()],
  },
  name: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  typology: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(10)],
  },
  address1: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  address2: {
    default: "",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  postalCode: {
    default: "",
    required: true,
    rules: [v.isPostalCode()],
  },
  city: {
    required: true,
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  phone: {
    default: "",
    pre: [v.removeAllSpaces],
    rules: [v.isPhone()],
  },
  email: {
    default: "",
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
  url: {
    default: "",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },
  shortDesc: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(280)],
    post: [v.trim],
  },
  fullDesc: { default: "", rules: [v.isString()], post: [v.trim] },
};
