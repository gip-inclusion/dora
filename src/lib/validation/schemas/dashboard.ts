import * as v from "../schema-utils";
import { SIREN_FRANCE_TRAVAIL } from "$lib/consts";

function checkFranceTravailRestrictions(msg = "") {
  return (_name, value, data) => ({
    valid: data.siret.startsWith(SIREN_FRANCE_TRAVAIL)
      ? !!(
          value.endsWith("@pole-emploi.fr") ||
          value.endsWith("@francetravail.fr") ||
          value.endsWith("beta.gouv.fr")
        )
      : true,
    msg:
      msg ||
      `Veuillez saisir une adresse en @francetravail.fr ou @pole-emploi.fr`,
  });
}

export const addUserSchema = {
  email: {
    label: "Courriel",
    default: "",
    rules: [v.isEmail(), checkFranceTravailRestrictions(), v.maxStrLength(254)],
    post: [v.lower, v.trim],
    maxLength: 254,
    required: true,
  },
  level: {
    label: "Permissions",
    default: "",
    rules: [
      v.isString(),
      (name, value, _data) => ({
        valid: value === "user" || value === "admin",
        msg: `Choix incorrect`,
      }),
    ],
    required: true,
  },
};

export const modifyUserSchema = {
  name: {
    label: "Nom",
    default: "",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
    maxLength: 255,
    readonly: true,
  },
  email: {
    label: "Courriel",
    default: "",
    rules: [v.isEmail(), v.maxStrLength(254)],
    post: [v.lower, v.trim],
    maxLength: 254,
    readonly: true,
  },
  level: {
    label: "Permissions",
    default: "",
    rules: [
      v.isString(),
      (name, value, _data) => ({
        valid: value === "user" || value === "admin",
        msg: `Choix incorrect`,
      }),
    ],
    required: true,
  },
};
