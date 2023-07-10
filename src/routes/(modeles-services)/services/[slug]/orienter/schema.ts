import * as v from "$lib/validation/schema-utils";

export const orientationStep1Schema: v.Schema = {
  situation: {
    label:
      "Cochez les éléments correspondants à la situation du ou de la bénéficiaire",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(480)])],
    required: true,
  },

  situationOther: {
    default: "",
    post: [v.trim],
    rules: [v.isString(), v.maxStrLength(480)],
    maxLength: 480,
    required: (data) => {
      return data?.situation?.includes("other");
    },
  },

  requirements: {
    label: "Cochez les critères auxquels le ou la bénéficiaire répond",
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(480)])],
  },
};

export const orientationStep2Schema: v.Schema = {
  prescriberStructure: {
    label: "Confirmez votre structure",
    rules: [v.isString(), v.maxStrLength(50)],
    required: true,
  },
  referentLastName: {
    label: "Nom",
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
    required: true,
    maxLength: 140,
  },
  referentFirstName: {
    label: "Prénom",
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
    required: true,
    maxLength: 140,
  },
  referentPhone: {
    label: "Téléphone",
    default: "",
    pre: [v.removeAllNonDigits],
    rules: [v.isPhone()],
    maxLength: 10,
    required: true,
  },
  referentEmail: {
    label: "E-mail",
    default: "",
    rules: [v.isEmail(), v.maxStrLength(254)],
    post: [v.lower, v.trim],
    maxLength: 254,
    required: true,
  },

  beneficiaryLastName: {
    label: "Nom",
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
    required: true,
    maxLength: 140,
  },
  beneficiaryFirstName: {
    label: "Prénom",
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
    required: true,
    maxLength: 140,
  },
  beneficiaryPhone: {
    label: "Téléphone",
    default: "",
    pre: [v.removeAllNonDigits],
    rules: [v.isPhone()],
    maxLength: 10,
    required: (data) => {
      return data?.beneficiaryContactPreferences?.includes("TELEPHONE");
    },
  },
  beneficiaryEmail: {
    label: "E-mail",
    default: "",
    rules: [v.isEmail(), v.maxStrLength(254)],
    post: [v.lower, v.trim],
    maxLength: 254,
    required: (data) => {
      return data?.beneficiaryContactPreferences?.includes("EMAIL");
    },
  },
  beneficiaryContactPreferences: {
    label: "Préférence de contact",
    default: [],
    rules: [v.isArray([v.isString()])],
    required: true,
  },
  beneficiaryOtherContactMethod: {
    label: "Autre méthode de contact",
    default: "",
    rules: [v.isString(), v.maxStrLength(280)],
    maxLength: 280,
    post: [v.trim],
    required: (data) => {
      return data?.beneficiaryContactPreferences?.includes("AUTRE");
    },
  },
  beneficiaryAvailability: {
    label: "Disponibilité",
    default: null,
    rules: [v.isDate()],
    post: [v.nullEmpty],
  },
  orientationReasons: {
    rules: [v.isString(), v.maxStrLength(600)],
    maxLength: 600,
    post: [v.trim],
  },
  attachments: {
    rules: [],
  },
};
