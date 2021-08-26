import * as v from "./utils";

const shape1 = {
  structure: {
    default: null,
    required: true,
    rules: [v.isString(), v.maxStrLength(50)],
  },
  category: {
    default: [],
    required: true,
    rules: [v.isString(), v.maxStrLength(2)],
  },
  subcategories: {
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(6)]), v.arrNotEmpty()],
  },
  kinds: {
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(2)]), v.arrNotEmpty()],
  },
  isCommonLaw: {
    default: false,
    rules: [v.isBool()],
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
  fullDesc: { default: "", rules: [v.isString()], post: [v.trim] },
};

const shape2 = {
  accessConditions: {
    default: [],
    rules: [v.isArray([v.isPK()])],
  },
  concernedPublic: {
    default: [],
    rules: [v.isArray([v.isPK()])],
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
      v.maxStrLength(140),
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
    rules: [v.isArray([v.isString(), v.maxStrLength(2)])],
  },
  beneficiariesAccessModesOther: {
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(280),
      (name, value, data) => ({
        valid: data.beneficiariesAccessModes.includes("OT")
          ? !!value.length
          : true,
        msg: `Ce champ est requis`,
      }),
    ],
  },
  coachOrientationModes: {
    default: [],
    required: true,
    rules: [v.isArray([v.isString(), v.maxStrLength(2)]), v.arrNotEmpty()],
  },
  coachOrientationModesOther: {
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(280),
      (name, value, data) => ({
        valid: data.coachOrientationModes.includes("OT")
          ? !!value.length
          : true,
        msg: `Ce champ est requis`,
      }),
    ],
  },
  requirements: {
    default: [],
    rules: [v.isArray([v.isPK()])],
  },
  credentials: {
    default: [],
    rules: [v.isArray([v.isPK()])],
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
    pre: [v.removeAllSpaces],
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
    rules: [v.isArray([v.isString(), v.maxStrLength(2)]), v.arrNotEmpty()],
  },
  remoteUrl: {
    default: "",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
  },
  city: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
  },
  address1: {
    default: "",
    required: true,
    rules: [v.isString(), v.maxStrLength(255)],
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
    required: true,
    rules: [v.isPostalCode()],
  },
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
  recurrence: {
    default: "",
    rules: [v.isString(), v.maxStrLength(2)],
  },
  recurrenceOther: {
    default: "",
    rules: [
      v.isString(),
      v.maxStrLength(140),
      (name, value, data) => ({
        valid: data.recurrence === "OT" ? value.length : true,
        msg: `Ce champ est requis`,
      }),
    ],
    post: [v.trim],
  },
  suspensionCount: {
    default: null,
    nullable: true,
    rules: [v.isInteger(), v.minNum(1)],
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
