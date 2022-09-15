/* eslint-disable */

import { INVALID_ERROR_MESSAGE } from "$lib/utils/structure";

// From https://github.com/jquense/yup/blob/03584f6758ff43409113c41f58fd41e065aa18a3/src/string.ts
const urlRegexp =
  /^((https?|ftp):)?\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;

const emailRegexp =
  /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i;

const phoneRegexp = /^\d{10}$/u;

const postalCodeRegexp = /^\d[0-9abAB]\d{3}$/u;

export const siretRegexp = /^\d{14}$/u;
/* eslint-enable */

// ----- Rules

export function isString(msg) {
  return (name, value, _data) => ({
    valid: typeof value === "string",
    msg: msg || `Ce champ doit être une chaine de caractères`, // TODO: this is not a valid enduser message
  });
}

export function isBool(msg) {
  return (name, value, _data) => ({
    valid: typeof value === "boolean",
    msg: msg || `Ce champ doit être un booléen`, // TODO: this is not a valid enduser message
  });
}

export function isInteger(msg) {
  return (name, value, _data) => ({
    valid: Number.isInteger(value),
    msg: msg || `Ce champ doit être un nombre entier`,
  });
}

export function isDate(msg) {
  return (name, value, _data) => ({
    // TODO: that's probably not safe enough. Use Luxon?
    // https://stackoverflow.com/questions/7445328/check-if-a-string-is-a-date-value
    valid:
      typeof value === "string" &&
      (value === "" || new Date(value) !== "Invalid Date"),
    msg: msg || `Veuillez saisir une date valide`,
  });
}

export function isURL(msg) {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" && (value === "" || !!value.match(urlRegexp)),
    msg: msg || `Veuillez saisir une URL valide (ex: https://exemple.fr)`,
  });
}

export function isEmail(msg) {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" && (value === "" || !!value.match(emailRegexp)),
    msg:
      msg ||
      `Veuillez saisir une adresse courriel valide (ex: nom.prenom@organisation.fr)`,
  });
}

export function isPhone(msg) {
  return (name, value, _data) => ({
    valid: typeof value === "string" && value.length <= 10,
    // Some numbers only have 4 digits (Pole Emploi or La CAF for example)
    // And we might have stranger cases, like extension numbers.
    // So for now, just ensure we get a string!
    // typeof value === "string" && (value === "" || !!value.match(phoneRegexp)),
    msg:
      msg ||
      `Veuillez saisir un numéro de téléphone valide (ex: 06 00 00 00 00 ou  0600000000`,
  });
}

export function isPostalCode(msg) {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" &&
      (value === "" || !!value.match(postalCodeRegexp)),
    msg: msg || `Veuillez saisir un code postal valide`,
  });
}

export function isSiret(msg) {
  return (name, value, _data) => ({
    valid:
      value == null ||
      (typeof value === "string" &&
        (value === "" || !!value.match(siretRegexp))),
    msg: msg || "Ce champ doit comporter 14 chiffres",
  });
}
export function isAccessLibreUrl(msg) {
  return (name, value, _data) => ({
    valid:
      value == null ||
      (typeof value === "string" &&
        (value === "" ||
          !!value.startsWith("https://acceslibre.beta.gouv.fr/"))),
    msg: msg || "L'URL doit commencer par https://acceslibre.beta.gouv.fr/",
  });
}
export function isNotStringInvalid(msg) {
  return (name, value, _data) => ({
    valid:
      value == null ||
      (typeof value === "string" &&
        (value === "" || value !== INVALID_ERROR_MESSAGE)),
    msg:
      msg ||
      "Horaires incomplètes. Veuillez finaliser la saisie de vos horaires, corriger les champs manquants ou incorrects.",
  });
}

export function isCustomizablePK(msg) {
  return (name, value, _data) => ({
    valid:
      (typeof value === "string" && value.length > 0) ||
      (Number.isInteger(value) && value > 0),
    msg: msg || `Ce champ doit être une clé étrangère`, // TODO: this is not a valid enduser message
  });
}

export function isArray(rules, msg) {
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
    };
  };
}

export function arrNotEmpty(msg) {
  return (name, value, _data) => ({
    valid: value.length > 0,
    msg: msg || `Veuillez selectionner au moins une option`,
  });
}

export function minStrLength(max, msg) {
  return (name, value, _data) => ({
    valid: value.length >= max,
    msg: msg || `Ce champ doit avoir au moins ${max} caractères`,
  });
}

export function maxStrLength(max, msg) {
  return (name, value, _data) => ({
    valid: value.length <= max,
    msg: msg || `Ce champ ne doit pas depasser ${max} caractères`,
  });
}

export function minNum(min, msg) {
  return (name, value, _data) => ({
    valid: value >= min,
    msg: msg || `Ce champ doit être une clé étrangère`, // TODO: this is not a valid enduser message
  });
}

// ----- Preprocessing
export function removeAllSpaces(value) {
  return value.replace(/ /g, "");
}

export function removeAllNonDigits(value) {
  return value.replace(/\D/gu, "");
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

export function formatSchema(schema, fields, fieldsRequired) {
  const schemaFormatted = {};
  Object.entries(schema).forEach(([key, value]) => {
    if (fields.includes(key)) {
      schemaFormatted[key] = {
        name: value.name,
        default: value.default,
        pre: value.pre,
        rules: value.rules,
        post: value.post,
        dependents: value.dependents,
        required:
          (typeof schema[key].required === "boolean" && schema[key].required) ||
          fieldsRequired.includes(key),
      };
    }
  });

  return schemaFormatted;
}
