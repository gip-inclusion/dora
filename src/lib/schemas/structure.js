import * as yup from "yup";
import { setLocale } from "yup";

setLocale({
  mixed: {
    required: "Ce champ est requis",
  },
  string: {
    length: "Ce champ doit faire ${length} caractères",
    min: "Ce champ ne doit pas avoir moins de ${min} caractères",
    max: "Ce champ ne doit pas dépasser ${max} caractères",
    email:
      "Veuillez saisir une adresse e-mail valide (ex: nom.prenom@organisation.fr)",
    url: "Veuillez saisir une URL valide (ex: https://exemple.fr)",
  },
});

export default yup.object().shape({
  siret: yup
    .string()
    .matches(/^\d{14}$/u, "Ce champ doit comporter 14 chiffres")
    .required(),
  name: yup.string().max(255).required(),
  typology: yup.string().ensure().max(10).required(),
  address1: yup.string().max(255).required(),
  address2: yup.string().max(255),
  postalCode: yup
    .string()
    .matches(/^\d[0-9abAB]\d{3}$/u, "Veuillez saisir un code postal valide")
    .length(5)
    .required(),
  city: yup.string().max(255).required(),
  phone: yup.string().max(10),
  email: yup.string().max(254).email().required(),
  url: yup.string().max(200).url(),
  shortDesc: yup.string().max(280).required(),
  fullDesc: yup.string(),
});
