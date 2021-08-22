/* eslint-disable */
// From https://github.com/jquense/yup/blob/03584f6758ff43409113c41f58fd41e065aa18a3/src/string.ts
const urlRegexp =
  /^((https?|ftp):)?\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;

const emailRegexp =
  /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i;

const phoneRegexp = /^\d{10}$/u;

const postalCodeRegexp = /^\d[0-9abAB]\d{3}$/u;
/* eslint-enable */

function isString(msg) {
  return (name, value, _data) => ({
    valid: typeof value === "string",
    msg: msg || `Ce champ doit être une chaine de caractères`, // TODO: this is not a valid enduser message
  });
}

function isBool(msg) {
  return (name, value, _data) => ({
    valid: typeof value === "boolean",
    msg: msg || `Ce champ doit être un booléen`, // TODO: this is not a valid enduser message
  });
}

function isInteger(msg) {
  return (name, value, _data) => ({
    valid: Number.isInteger(value),
    msg: msg || `Ce champ doit être un nombre entier`,
  });
}

function isDate(msg) {
  return (name, value, _data) => ({
    // TODO: that's probably not safe enough. Use Luxon?
    // https://stackoverflow.com/questions/7445328/check-if-a-string-is-a-date-value
    valid:
      typeof value === "string" &&
      (value === "" || new Date(value) !== "Invalid Date"),
    msg: msg || `Veuillez saisir une date valide`,
  });
}

function isURL(msg) {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" && (value === "" || !!value.match(urlRegexp)),
    msg: msg || `Veuillez saisir une URL valide (ex: https://exemple.fr)`,
  });
}

function isEmail(msg) {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" && (value === "" || !!value.match(emailRegexp)),
    msg:
      msg ||
      `Veuillez saisir une adresse e-mail valide (ex: nom.prenom@organisation.fr)`,
  });
}

function isPhone(msg) {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" && (value === "" || !!value.match(phoneRegexp)),
    msg:
      msg ||
      `Veuillez saisir un numéro de téléphone valide (ex: 06 00 00 00 00 ou  0600000000`,
  });
}
function isPostalCode(msg) {
  return (name, value, _data) => ({
    valid:
      typeof value === "string" &&
      (value === "" || !!value.match(postalCodeRegexp)),
    msg: msg || `Veuillez saisir un code postal valide`,
  });
}

function isPK(msg) {
  return (name, value, _data) => ({
    valid: Number.isInteger(value) && value > 0,
    msg: msg || `Ce champ doit être une clé étrangère`, // TODO: this is not a valid enduser message
  });
}

function isArray(rules, msg) {
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

function arrNotEmpty(msg) {
  return (name, value, _data) => ({
    valid: value.length > 0,
    msg: msg || `Veuillez selectionner au moins une option`,
  });
}

function maxStrLength(max, msg) {
  return (name, value, _data) => ({
    valid: value.length <= max,
    msg: msg || `Ce champ ne doit pas depasser ${max} caractères`,
  });
}

function minNum(min, msg) {
  return (name, value, _data) => ({
    valid: value >= min,
    msg: msg || `Ce champ doit être une clé étrangère`, // TODO: this is not a valid enduser message
  });
}

// ----- Preprocessing
function removeAllSpaces(value) {
  return value.replaceAll(" ", "");
}

// ----- Postprocessing
function lower(value) {
  return value.toLowerCase();
}

function trim(value) {
  return value.trim();
}

// ------
const shape1 = {
  structure: {
    default: null,
    required: true,
    rules: [isString(), maxStrLength(50)],
  },
  categories: {
    default: [],
    required: true,
    rules: [isArray([isString(), maxStrLength(2)]), arrNotEmpty()],
  },
  subcategories: {
    default: [],
    required: true,
    rules: [isArray([isString(), maxStrLength(3)]), arrNotEmpty()],
  },
  kinds: {
    default: [],
    required: true,
    rules: [isArray([isString(), maxStrLength(2)]), arrNotEmpty()],
  },
  isCommonLaw: {
    default: false,
    rules: [isBool()],
  },
  name: {
    default: "",
    required: true,

    rules: [isString(), maxStrLength(140)],
    post: [trim],
  },
  shortDesc: {
    default: "",
    required: true,

    rules: [isString(), maxStrLength(280)],
    post: [trim],
  },
  fullDesc: { default: "", rules: [isString()], post: [trim] },
};

const shape2 = {
  accessConditions: {
    default: [],
    rules: [isArray([isPK()])],
  },
  concernedPublic: {
    default: [],
    rules: [isArray([isPK()])],
  },
  isCumulative: {
    default: true,
    rules: [isBool()],
  },
  hasFee: {
    default: false,
    rules: [isBool()],
  },
  feeDetails: {
    default: "",
    post: [trim],
    rules: [
      isString(),
      maxStrLength(140),
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
    required: true,
    rules: [isArray([isString(), maxStrLength(2)]), arrNotEmpty()],
  },
  beneficiariesAccessModesOther: {
    default: "",
    rules: [
      isString(),
      maxStrLength(280),
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
    rules: [isArray([isString(), maxStrLength(2)]), arrNotEmpty()],
  },
  coachOrientationModesOther: {
    default: "",
    rules: [
      isString(),
      maxStrLength(280),
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
    rules: [isArray([isPK()])],
  },
  credentials: {
    default: [],
    rules: [isArray([isPK()])],
  },
  forms: {
    default: [],
    rules: [isArray([isString(), maxStrLength(1024)])],
  },
  onlineForm: {
    default: "",
    rules: [isURL(), maxStrLength(200)],
    post: [trim],
  },
};

const shape4 = {
  contactName: {
    default: "",
    rules: [isString(), maxStrLength(140)],
    post: [trim],
  },
  contactPhone: {
    default: "",
    pre: [removeAllSpaces],
    rules: [isPhone()],
  },
  contactEmail: {
    default: "",
    rules: [isEmail(), maxStrLength(255)],
    post: [lower, trim],
  },
  isContactInfoPublic: {
    default: false,
    rules: [isBool()],
  },

  locationKinds: {
    default: [],
    required: true,
    rules: [isArray([isString(), maxStrLength(2)]), arrNotEmpty()],
  },
  remoteUrl: {
    default: "",
    rules: [isURL(), maxStrLength(200)],
    post: [trim],
  },
  city: {
    default: "",
    required: true,

    rules: [isString(), maxStrLength(255)],
    post: [trim],
  },
  address1: {
    default: "",
    required: true,

    rules: [isString(), maxStrLength(255)],
    post: [trim],
  },
  address2: {
    default: "",
    rules: [isString(), maxStrLength(255)],
    post: [trim],
  },
  postalCode: {
    default: "",
    required: true,
    rules: [isPostalCode()],
  },
  startDate: {
    default: null,
    nullable: true,
    rules: [isDate()],
    dependents: ["endDate"],
  },
  endDate: {
    default: null,
    nullable: true,
    rules: [
      isDate(),
      (name, value, data) => ({
        valid: !data.startDate || new Date(value) >= new Date(data.startDate),
        msg: `La date de fin doit être postérieure à la date de début`,
      }),
    ],
  },
  recurrence: {
    default: "",
    rules: [isString(), maxStrLength(2)],
  },
  recurrenceOther: {
    default: "",
    rules: [
      isString(),
      maxStrLength(140),
      (name, value, data) => ({
        valid: data.recurrence === "OT" ? value.length : true,
        msg: `Ce champ est requis`,
      }),
    ],
    post: [trim],
  },
  suspensionCount: {
    default: null,
    nullable: true,
    rules: [isInteger(), minNum(1)],
  },
  suspensionDate: {
    default: null,
    nullable: true,
    rules: [isDate()],
  },
};

export const step1 = shape1;
export const step2 = shape2;
export const step3 = shape3;
export const step4 = shape4;

export default {
  ...shape1,
  ...shape2,
  ...shape3,
  ...shape4,
};
