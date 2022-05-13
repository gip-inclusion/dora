import * as v from "./utils";

const shape1 = {
  isDraft: {
    name: "brouillon",
    default: true,
    rules: [v.isBool()],
  },
  structure: {
    name: "structure",
    default: null,
    required: true,
    rules: [v.isString(), v.maxStrLength(50)],
  },
  categories: {
    name: "thématiques",
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(255)]), v.arrNotEmpty()],
  },
  subcategories: {
    name: "besoins",
    default: [],
    required: false,
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  kinds: {
    name: "types",
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(255)]), v.arrNotEmpty()],
  },
  name: {
    name: "nom",
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  shortDesc: {
    name: "résumé",
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(280)],
    post: [v.trim],
  },
  recurrence: {
    name: "fréquence et horaires",
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  fullDesc: {
    name: "description",
    default: "",
    rules: [v.isString()],
    post: [v.trim],
  },
};

const shape2 = {
  accessConditions: {
    name: "critères",
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  concernedPublic: {
    name: "profils",
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  requirements: {
    name: "pré-requis ou compétences",
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  isCumulative: {
    name: "cumulable",
    default: true,
    rules: [v.isBool()],
  },
  hasFee: {
    name: "frais à charge",
    default: false,
    rules: [v.isBool()],
  },
  feeDetails: {
    name: "frais à charge (détail)",
    default: "",
    post: [v.trim],
    rules: [
      v.isString(),
      (name, value, data) => ({
        valid: !data.hasFee || value.length,
        msg: `Information requise`,
      }),
    ],
  },
};

const shape3 = {
  beneficiariesAccessModes: {
    name: "pour les bénéficiaires",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  beneficiariesAccessModesOther: {
    name: "pour les bénéficiaires (autre)",
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(280),
      (name, value, data) => ({
        valid: data.beneficiariesAccessModes.includes("autre")
          ? !!value.length
          : true,
        msg: `Information requise`,
      }),
    ],
  },
  coachOrientationModes: {
    name: "pour les accompagnateurs",
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(255)]), v.arrNotEmpty()],
  },
  coachOrientationModesOther: {
    name: "pour les accompagnateurs (autre)",
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(280),
      (name, value, data) => ({
        valid: data.coachOrientationModes.includes("autre")
          ? !!value.length
          : true,
        msg: `Information requise`,
      }),
    ],
  },

  credentials: {
    name: "justificatifs à fournir",
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  forms: {
    name: "documents à compléter",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(1024)])],
  },
  onlineForm: {
    name: "lien",
    default: "",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },
};

const shape4 = {
  contactName: {
    name: "prénom et nom",
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  contactPhone: {
    name: "téléphone",
    default: "",
    pre: [v.removeAllNonDigits],
    rules: [v.isPhone()],
  },
  contactEmail: {
    name: "email",
    default: "",
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
  isContactInfoPublic: {
    name: "rendre les informations publiques",
    default: false,
    rules: [v.isBool()],
  },

  locationKinds: {
    name: "lieu de déroulement",
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(255)]), v.arrNotEmpty()],
  },
  remoteUrl: {
    name: "lien visioconférence",
    default: "",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },
  city: {
    name: "ville",
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(255),
      (name, value, data) => ({
        valid: data.locationKinds.includes("en-presentiel")
          ? !!value.length
          : true,
        msg: `Information requise`,
      }),
    ],
    post: [v.trim],
  },
  address1: {
    name: "adresse",
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(255),
      (name, value, data) => ({
        valid: data.locationKinds.includes("en-presentiel")
          ? !!value.length
          : true,
        msg: `Information requise`,
      }),
    ],
    post: [v.trim],
    dependents: ["postalCode"],
  },
  address2: {
    name: "complément d'adresse",
    default: "",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  postalCode: {
    name: "code postal",
    default: "",
    rules: [
      v.isPostalCode(),
      (name, value, data) => ({
        valid: data.locationKinds.includes("en-presentiel")
          ? !!value.length
          : true,
        msg: `Information requise`,
      }),
    ],
  },
  diffusionZoneType: {
    name: "territoire",
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(10)],
  },

  diffusionZoneDetails: {
    name: "nom du territoire",
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(9),
      (name, value, data) => ({
        valid: data.diffusionZoneType !== "country" ? !!value.length : true,
        msg: `Information requise`,
      }),
    ],
  },
  qpvOrZrr: {
    name: "uniquement QPV ou ZRR",
    default: false,
    rules: [v.isBool()],
  },
  startDate: {
    name: "date de début",
    default: null,
    nullable: true,
    rules: [v.isDate()],
    dependents: ["endDate"],
    post: [v.nullEmpty],
  },
  endDate: {
    name: "date de fin",
    default: null,
    nullable: true,
    rules: [
      v.isDate(),
      (name, value, data) => ({
        valid: !data.startDate || new Date(value) >= new Date(data.startDate),
        msg: `La date de fin doit être postérieure à la date de début`,
      }),
    ],
    post: [v.nullEmpty],
  },
  suspensionDate: {
    name: "date de fin",
    default: null,
    nullable: true,
    rules: [v.isDate()],
    post: [v.nullEmpty],
  },
};

export const step1Schema = shape1;
export const step2Schema = shape2;
export const step3Schema = shape3;
export const step4Schema = shape4;

export default {
  ...shape1,
  ...shape2,
  ...shape3,
  ...shape4,
};

export const draftServiceSchema = {
  structure: {
    name: "structure",
    required: true,
    rules: [v.isString(), v.maxStrLength(50)],
  },
  name: {
    name: "nom",
    required: true,
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  categories: {
    name: "thématiques",
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  subcategories: {
    name: "besoins",
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  kinds: {
    name: "types",
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  shortDesc: {
    name: "résumé",
    rules: [v.isString(), v.maxStrLength(280)],
    post: [v.trim],
  },
  recurrence: {
    name: "fréquence et horaires",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  fullDesc: { name: "description", rules: [v.isString()], post: [v.trim] },

  accessConditions: {
    name: "critères",
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  concernedPublic: {
    name: "profils",
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  requirements: {
    name: "pré-requis ou compétences",
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  isCumulative: {
    name: "cumulable",
    rules: [v.isBool()],
  },
  hasFee: {
    name: "frais à charge",
    rules: [v.isBool()],
  },
  feeDetails: {
    name: "détail des frais",
    post: [v.trim],
    rules: [v.isString()],
  },

  beneficiariesAccessModes: {
    name: "pour le bénéficiaire",
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  beneficiariesAccessModesOther: {
    name: "pour le bénéficiaire (autre)",
    rules: [v.isString(), v.maxStrLength(280)],
  },
  coachOrientationModes: {
    name: "pour l'accompagnateur",
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  coachOrientationModesOther: {
    name: "pour l'accompagnateur (autre)",
    rules: [v.isString(), v.maxStrLength(280)],
  },

  credentials: {
    name: "justificatifs à fournir",
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  forms: {
    name: "documents à compléter",
    rules: [v.isArray([v.isString(), v.maxStrLength(1024)])],
  },
  onlineForm: {
    name: "lien",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },

  contactName: {
    name: "prénom et nom",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  contactPhone: {
    name: "téléphone",
    pre: [v.removeAllNonDigits],
    rules: [v.isPhone()],
  },
  contactEmail: {
    name: "email",
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
  isContactInfoPublic: {
    name: "rendre les informations publiques",
    rules: [v.isBool()],
  },

  locationKinds: {
    name: "lieu de déroulement",
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  remoteUrl: {
    name: "lien visioconférence",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },
  city: {
    name: "ville",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  address1: {
    name: "adresse",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
    dependents: ["postalCode"],
  },
  address2: {
    name: "complément d’adresse",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  postalCode: {
    name: "code postal",
    rules: [v.isPostalCode()],
  },
  diffusionZoneType: {
    name: "territoire",
    default: "",
    rules: [v.isString(), v.maxStrLength(10)],
  },
  diffusionZoneDetails: {
    name: "nom du territoire",
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(9),
      (name, value, data) => ({
        valid:
          data.diffusionZoneType === "" ||
          (data.diffusionZoneType !== "country" ? !!value.length : true),
        msg: `Information requise`,
      }),
    ],
  },
  qpvOrZrr: {
    name: "uniquement QPV ou ZRR",
    default: false,
    rules: [v.isBool()],
  },
  startDate: {
    name: "date de début",
    nullable: true,
    rules: [v.isDate()],
    post: [v.nullEmpty],
  },
  endDate: {
    name: "date de fin",
    nullable: true,
    rules: [v.isDate()],
    post: [v.nullEmpty],
  },
  suspensionDate: {
    name: "date de fin",
    nullable: true,
    rules: [v.isDate()],
    post: [v.nullEmpty],
  },
};

export const suggestionSchema = {
  fullName: {
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
  message: {
    default: "",
    required: true,
    rules: [v.isString()],
  },
};
