import "./schema-i18n.js";
import { object, string, array, boolean, number, date } from "yup";
import { phone, postalCode } from "./schema-utils.js";

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
  accessConditions: number().positive(),
  concernedPublic: number().positive(),
  isCumulative: boolean(),
  hasFee: boolean(),
  feeDetails: string().max(140).trim(),
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
  requirements: number().positive(),
  credentials: number().positive(),
  forms: array(string().max(1024)),
  onlineForm: string().max(280).trim(),
};

const shape4 = {
  contactName: string().max(140).required().trim(),
  contactPhone: phone().required(),
  contactEmail: string().max(254).email().required().lowercase().trim(),
  isContactInfoPublic: boolean(),
  locationKind: array(string().max(2)).required().min(1),
  remoteUrl: string().max(200).url().trim(),
  city: string().max(255).required().trim(),
  address1: string().max(255).required().trim(),
  address2: string().max(255).trim(),
  postalCode: postalCode(),
  isTimeLimited: boolean(),
  startDate: date(),
  endDate: date(),
  recurrence: string().max(2),
  recurrenceOther: string().max(140).trim(),
  suspensionCount: number().positive().min(1),
  suspensionDate: date(),
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
