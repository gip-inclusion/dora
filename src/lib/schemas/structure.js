import "./schema-i18n.js";
import { object, string } from "yup";
import { phone, postalCode } from "./schema-utils.js";

export default object().shape({
  siret: string()
    .matches(/^\d{14}$/u, "Ce champ doit comporter 14 chiffres")
    .required(),
  name: string().max(255).required().trim(),
  typology: string().ensure().max(10).required(),
  address1: string().max(255).required().trim(),
  address2: string().max(255).trim(),
  postalCode: postalCode().required(),
  city: string().max(255).required().trim(),
  phone: phone(),
  email: string().max(254).email().required().lowercase().trim(),
  url: string().max(200).url().trim(),
  shortDesc: string().max(280).required().trim(),
  fullDesc: string().trim(),
});
