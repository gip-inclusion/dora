import { setLocale } from "yup";

setLocale({
  mixed: {
    required: "Ce champ est requis",
    notType: ({ _path, type, _value, _originalValue }) => {
      let locType;
      switch (type) {
        case "date":
          locType = "une date";
          break;
        default:
          locType = "une valeur";
      }
      return `Veuillez saisir ${locType} valide`;
    },
  },
  string: {
    length: "Ce champ doit faire ${length} caractères",
    min: "Ce champ ne doit pas avoir moins de ${min} caractères",
    max: "Ce champ ne doit pas dépasser ${max} caractères",
    email:
      "Veuillez saisir une adresse e-mail valide (ex: nom.prenom@organisation.fr)",
    url: "Veuillez saisir une URL valide (ex: https://exemple.fr)",
  },
  array: {
    min: ({ min }) =>
      `Veuillez selectionner au moins ${min} option${min > 1 ? "s" : ""}`,
  },
  number: {
    positive: "Veuillez saisir un nombre positif",
    min: "Veuillez saisir un nombre superieur ou égal à ${min}",
  },
  date: {},
});
