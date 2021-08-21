import "./schema-i18n.js";
import { object, string, array, boolean, number, date } from "yup";
import { phone, postalCode, isoDate } from "./schema-utils.js";

const shape1 = {
  structure: string().max(50).required(),
  categories: array(string().max(2)).required().min(1),
  subcategories: array(string().max(3)).required().min(1),
  kinds: array(string().max(2)).required().min(1),
  isCommonLaw: boolean(),
  name: string().max(140).required().trim(),
  shortDesc: string().max(280).required().trim(),
  fullDesc: string().trim(),
};

const shape2 = {
  accessConditions: array(number().integer()),
  concernedPublic: array(number().integer()),
  isCumulative: boolean(),
  hasFee: boolean(),
  feeDetails: string()
    .when("hasFee", {
      is: true,
      then: string().max(140).required(),
    })
    .trim(),
};

const shape3 = {
  beneficiariesAccessModes: array(string().max(2)).required().min(1),
  beneficiariesAccessModesOther: string().when("beneficiariesAccessModes", {
    is: (value) => value.includes("OT"),
    then: string().max(280).required(),
  }),
  coachOrientationModes: array(string().max(2)).required().min(1),
  coachOrientationModesOther: string().when("coachOrientationModes", {
    is: (value) => value.includes("OT"),
    then: string().max(280).required(),
  }),
  requirements: array(number().integer()),
  credentials: array(number().integer()),
  forms: array(string().max(1024)),
  onlineForm: string().max(280).url().trim(),
};

const shape4 = {
  contactName: string().max(140).trim(),
  contactPhone: phone(),
  contactEmail: string().max(254).email().lowercase().trim(),
  isContactInfoPublic: boolean(),
  locationKinds: array(string().max(2)).required().min(1),
  remoteUrl: string().max(200).url().trim(),
  city: string().max(255).required().trim(),
  address1: string().max(255).required().trim(),
  address2: string().max(255).trim(),
  postalCode: postalCode(),
  isTimeLimited: boolean(),
  // startDate: isoDate().nullable(),
  // endDate: isoDate().nullable(),
  recurrence: string().max(2),
  recurrenceOther: string().max(140).trim(),
  suspensionCount: number().nullable().integer().positive().min(1),
  // suspensionDate: isoDate().nullable(),
};

export const step1 = object().shape(shape1);

export const step2 = object().shape(shape2);

export const step3 = object().shape(shape3);

export const step4 = object().shape(shape4);

export default object().shape({
  ...shape1,
  ...shape2,
  ...shape3,
  ...shape4,
});
