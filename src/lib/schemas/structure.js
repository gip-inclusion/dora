import * as v from "./utils";

export default {
  siret: {
    default: "",
    name: "siret",
    rules: [v.isSiret()],
  },
  name: {
    default: "",
    name: "nom",
    required: true,
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  typology: {
    name: "typologie",
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(255)],
  },
  address1: {
    default: "",
    name: "adresse",
    required: true,
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  address2: {
    default: "",
    name: "complément d’adresse",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  postalCode: {
    default: "",
    name: "code postal",
    required: true,
    rules: [v.isPostalCode()],
  },
  city: {
    required: true,
    name: "ville",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  phone: {
    default: "",
    name: "téléphone",
    pre: [v.removeAllNonDigits],
    rules: [v.isPhone()],
  },
  email: {
    default: "",
    name: "courriel",
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
  url: {
    default: "",
    name: "site web",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },
  shortDesc: {
    default: "",
    name: "résumé",
    required: true,
    rules: [v.isString(), v.maxStrLength(280)],
    post: [v.trim],
  },
  fullDesc: { default: "", rules: [v.isString()], post: [v.trim] },
};
