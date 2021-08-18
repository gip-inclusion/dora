import { string } from "yup";

export const phone = () =>
  string()
    .transform((value, _originalValue) => value.replaceAll(" ", ""))
    .matches(/^\d{10}$/u, {
      message:
        "Veuillez saisir un numéro de téléphone valide (ex: 06 00 00 00 00 ou  0600000000",
      excludeEmptyString: true,
    });

export const postalCode = () =>
  string()
    .matches(/^\d[0-9abAB]\d{3}$/u, "Veuillez saisir un code postal valide")
    .length(5);
