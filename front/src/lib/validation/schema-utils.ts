/* eslint-disable */
import type { ServicesOptions } from "$lib/types";
import { INVALID_OPENING_HOURS_MARKER } from "$lib/utils/opening-hours/constants";

const urlRegexp = /^(https?|ftp):\/\/[^\s]{1,2000}$/;

// Prise sur https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address
const emailRegexp =
  /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

const postalCodeRegexp = /^\d[0-9abAB]\d{3}$/u;

export const siretRegexp = /^\d{14}$/u;

export const franceTravailNumberRegexp = /^\d{11}$/u;
/* eslint-enable */

export type Action<T> = (value: T) => T;

export type Rule = (
  name: string,
  value: any,
  data?: any,
  servicesOptions?: ServicesOptions,
  schema?: any
) => {
  valid: boolean;
  msg: string;
};

export type SchemaRequirement = ((data: any) => boolean) | boolean;

export interface Shape<T> {
  rules: Rule[];
  default?: T;
  post?: Action<T>[];
  pre?: Action<T>[];
  required?: SchemaRequirement;
  label?: string;
  maxLength?: number;
  minNumber?: number;
  readonly?: boolean;
}

export interface Schema {
  [fieldName: string]: Shape<any>;
}

// ----- Rules

export function isString(msg = "") {
  return (name: string, value: any, _data) => ({
    valid: typeof value === "string",
    msg: msg || `Ce champ doit être une chaine de caractères`, // TODO: this is not a valid enduser message
  });
}

export function isBool(msg = "") {
  return (name, value, _data) => ({
    valid: typeof value === "boolean",
    msg: msg || `Ce champ doit être un booléen`, // TODO: this is not a valid enduser message
  });
}

export function isInteger(msg = "") {
  return (name, value, _data) => ({
    valid:
      value === undefined ||
      value === null ||
      value === "" ||
      Number.isInteger(value),
    msg: msg || `Ce champ doit être un nombre entier`,
  });
}

export function isPositiveInteger(msg = "") {
  return (name, value, _data) => {
    return {
      valid:
        value === undefined ||
        value === null ||
        value === "" ||
        (!isNaN(value) && value >= 0),
      msg: msg || `Ce champ doit être un nombre entier positif`,
    };
  };
}

export function minNum(min, msg = "") {
  return (name, value, _data) => ({
    valid:
      value === undefined || value === "" || (!isNaN(value) && value >= min),
    msg: msg || `Ce champ doit être supérieur ou égal à ${min}`,
  });
}

export function isDate(msg = "") {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" &&
      (value === "" || !isNaN(new Date(value).getTime())),
    msg: msg || `Veuillez saisir une date valide`,
  });
}

export function isURL(msg = "") {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" && (value === "" || !!value.match(urlRegexp)),
    msg: msg || `Veuillez saisir une URL valide (ex: https://exemple.fr)`,
  });
}

export function isEmail(msg = "") {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" && (value === "" || !!value.match(emailRegexp)),
    msg:
      msg ||
      `Veuillez saisir une adresse courriel valide (ex: nom.prenom@organisation.fr)`,
  });
}

export function isPhone(msg = "") {
  return (name, value, _data) => ({
    valid: typeof value === "string" && value.length <= 10,
    // Some numbers only have 4 digits (France Travail or La CAF for example)
    // And we might have stranger cases, like extension numbers.
    // So for now, just ensure we get a string!
    msg:
      msg || `Veuillez saisir un numéro de téléphone valide (ex: 0600000000)`,
  });
}

export function isPostalCode(msg = "") {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" &&
      (value === "" || !!value.match(postalCodeRegexp)),
    msg: msg || `Veuillez saisir un code postal valide`,
  });
}

export function isSiret(msg = "") {
  return (name, value, _data) => ({
    valid:
      value == null ||
      (typeof value === "string" &&
        (value === "" || !!value.match(siretRegexp))),
    msg: msg || "Format invalide. 14 chiffres attendus.",
  });
}

export function isFranceTravailNumber(msg = "") {
  return (name, value, _data) => ({
    valid:
      value == null ||
      (typeof value === "string" &&
        (value === "" || !!value.match(franceTravailNumberRegexp))),
    msg: msg || "Format invalide. 11 chiffres attendus.",
  });
}

export function isAccessLibreUrl(msg = "") {
  return (name, value, _data) => ({
    valid:
      value == null ||
      (typeof value === "string" &&
        (value === "" ||
          !!value.startsWith("https://acceslibre.beta.gouv.fr/"))),
    msg: msg || "L'URL doit commencer par https://acceslibre.beta.gouv.fr/",
  });
}

export function isCustomizablePK(msg = "") {
  return (name, value, _data) => ({
    valid:
      (typeof value === "string" && value.length > 0) ||
      (Number.isInteger(value) && value > 0),
    msg: msg || `Ce champ doit être une clé étrangère`, // TODO: this is not a valid enduser message
  });
}

export function isArray(rules: Rule[], msg = "") {
  return (name, value, data) => {
    if (!Array.isArray(value)) {
      return {
        valid: false,
        msg: msg || `Ce champ doit être un tableau`, // TODO: this is not a valid enduser message
      };
    }
    for (const childValue of value) {
      for (const rule of rules) {
        const result = rule(name, childValue, data);
        if (!result.valid) {
          return {
            valid: false,
            msg: result.msg,
          };
        }
      }
    }
    return {
      valid: true,
      msg,
    };
  };
}

export function arrNotEmpty(msg = "") {
  return (name, value, _data) => ({
    valid: value.length > 0,
    msg: msg || `Veuillez selectionner au moins une option`,
  });
}
export function arrMaxLength(max, msg = "") {
  return (name, value, _data) => ({
    valid: value.length <= max,
    msg: msg || `Vous ne pouvez pas sélectionner plus de ${max} options`,
  });
}

export function minStrLength(max, msg = "") {
  return (name, value, _data) => ({
    valid: value.length >= max,
    msg: msg || `Ce champ doit avoir au moins ${max} caractères`,
  });
}

export function maxStrLength(max, msg = "") {
  return (name, value, _data) => ({
    valid: value.length <= max,
    msg: msg || `Ce champ ne doit pas depasser ${max} caractères`,
  });
}

export function osmHoursNotContainsInvalid(msg = "") {
  return (name, value, _data) => ({
    valid: !value.toLowerCase().includes(INVALID_OPENING_HOURS_MARKER),
    msg:
      msg ||
      "Horaires incomplets. Veuillez finaliser la saisie de vos horaires, corriger les champs manquants ou incorrects.",
  });
}

// ----- Preprocessing
export function removeAllSpaces(value) {
  return value.replace(/ /g, "");
}

export function removeAllNonDigits(value) {
  return value.replace(/\D/gu, "");
}

export function toNumber(value) {
  if (isNaN(value)) {
    return undefined;
  }
  if (value === "") {
    return null;
  }
  return Number(value);
}

// ----- Postprocessing
export function lower(value) {
  return value.toLowerCase();
}

export function trim(value) {
  return value.trim();
}

export function nullEmpty(value) {
  return value === "" ? null : value;
}
