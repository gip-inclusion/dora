import * as v from "./utils";

const shape1 = {
  isDraft: {
    default: true,
    rules: [v.isBool()],
  },
  structure: {
    default: null,
    required: true,
    rules: [v.isString(), v.maxStrLength(50)],
  },
  categories: {
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(255)]), v.arrNotEmpty()],
  },
  subcategories: {
    default: [],
    required: false,
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  kinds: {
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(255)]), v.arrNotEmpty()],
  },
  name: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  shortDesc: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(280)],
    post: [v.trim],
  },
  recurrence: {
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  fullDesc: { default: "", rules: [v.isString()], post: [v.trim] },
};

const shape2 = {
  accessConditions: {
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  concernedPublic: {
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  requirements: {
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  isCumulative: {
    default: true,
    rules: [v.isBool()],
  },
  hasFee: {
    default: false,
    rules: [v.isBool()],
  },
  feeDetails: {
    default: "",
    post: [v.trim],
    rules: [
      v.isString(),
      (name, value, data) => ({
        valid: !data.hasFee || value.length,
        msg: `Ce champ est requis`,
      }),
    ],
  },
};

const shape3 = {
  beneficiariesAccessModes: {
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  beneficiariesAccessModesOther: {
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(280),
      (name, value, data) => ({
        valid: data.beneficiariesAccessModes.includes("autre")
          ? !!value.length
          : true,
        msg: `Ce champ est requis`,
      }),
    ],
  },
  coachOrientationModes: {
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(255)]), v.arrNotEmpty()],
  },
  coachOrientationModesOther: {
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(280),
      (name, value, data) => ({
        valid: data.coachOrientationModes.includes("autre")
          ? !!value.length
          : true,
        msg: `Ce champ est requis`,
      }),
    ],
  },

  credentials: {
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  forms: {
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(1024)])],
  },
  onlineForm: {
    default: "",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },
};

const shape4 = {
  contactName: {
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  contactPhone: {
    default: "",
    pre: [v.removeAllNonDigits],
    rules: [v.isPhone()],
  },
  contactEmail: {
    default: "",
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
  isContactInfoPublic: {
    default: false,
    rules: [v.isBool()],
  },

  locationKinds: {
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(255)]), v.arrNotEmpty()],
  },
  remoteUrl: {
    default: "",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },
  city: {
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(255),
      (name, value, data) => ({
        valid: data.locationKinds.includes("en-presentiel")
          ? !!value.length
          : true,
        msg: `Ce champ est requis`,
      }),
    ],
    post: [v.trim],
  },
  address1: {
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(255),
      (name, value, data) => ({
        valid: data.locationKinds.includes("en-presentiel")
          ? !!value.length
          : true,
        msg: `Ce champ est requis`,
      }),
    ],
    post: [v.trim],
    dependents: ["postalCode"],
  },
  address2: {
    default: "",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  postalCode: {
    default: "",
    rules: [
      v.isPostalCode(),
      (name, value, data) => ({
        valid: data.locationKinds.includes("en-presentiel")
          ? !!value.length
          : true,
        msg: `Ce champ est requis`,
      }),
    ],
  },
  diffusionZoneType: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(10)],
  },

  diffusionZoneDetails: {
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(9),
      (name, value, data) => ({
        valid: data.diffusionZoneType !== "country" ? !!value.length : true,
        msg: `Ce champ est requis`,
      }),
    ],
  },
  qpvOrZrr: { default: false, rules: [v.isBool()] },
  startDate: {
    default: null,
    nullable: true,
    rules: [v.isDate()],
    dependents: ["endDate"],
    post: [v.nullEmpty],
  },
  endDate: {
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
    required: true,
    rules: [v.isString(), v.maxStrLength(50)],
  },
  name: {
    required: true,
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  categories: {
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  subcategories: {
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  kinds: {
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  shortDesc: {
    rules: [v.isString(), v.maxStrLength(280)],
    post: [v.trim],
  },
  recurrence: {
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  fullDesc: { rules: [v.isString()], post: [v.trim] },

  accessConditions: {
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  concernedPublic: {
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  requirements: {
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  isCumulative: {
    rules: [v.isBool()],
  },
  hasFee: {
    rules: [v.isBool()],
  },
  feeDetails: {
    post: [v.trim],
    rules: [v.isString()],
  },

  beneficiariesAccessModes: {
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  beneficiariesAccessModesOther: {
    rules: [v.isString(), v.maxStrLength(280)],
  },
  coachOrientationModes: {
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  coachOrientationModesOther: {
    rules: [v.isString(), v.maxStrLength(280)],
  },

  credentials: {
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  forms: {
    rules: [v.isArray([v.isString(), v.maxStrLength(1024)])],
  },
  onlineForm: {
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },

  contactName: {
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
  },
  contactPhone: {
    pre: [v.removeAllNonDigits],
    rules: [v.isPhone()],
  },
  contactEmail: {
    rules: [v.isEmail(), v.maxStrLength(255)],
    post: [v.lower, v.trim],
  },
  isContactInfoPublic: {
    rules: [v.isBool()],
  },

  locationKinds: {
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
  },
  remoteUrl: {
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },
  city: {
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  address1: {
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
    dependents: ["postalCode"],
  },
  address2: {
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  postalCode: {
    rules: [v.isPostalCode()],
  },
  diffusionZoneType: {
    default: "",
    rules: [v.isString(), v.maxStrLength(10)],
  },
  diffusionZoneDetails: {
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(9),
      (name, value, data) => ({
        valid:
          data.diffusionZoneType === "" ||
          (data.diffusionZoneType !== "country" ? !!value.length : true),
        msg: `Ce champ est requis`,
      }),
    ],
  },
  qpvOrZrr: { default: false, rules: [v.isBool()] },
  startDate: {
    nullable: true,
    rules: [v.isDate()],
    post: [v.nullEmpty],
  },
  endDate: {
    nullable: true,
    rules: [v.isDate()],
    post: [v.nullEmpty],
  },
  suspensionDate: {
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
