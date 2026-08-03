import type { ModesMobilisation, PersonneMobilisatrice } from "$lib/types";

export const orderedModesMobilisationValues: Record<ModesMobilisation, number> =
  {
    "formulaire-dora": 0,
    "utiliser-lien-mobilisation": 1,
    "envoyer-un-courriel": 2,
    telephoner: 3,
    "se-presenter": 4,
  };

export const orderedMobilisableParValues: Record<
  PersonneMobilisatrice,
  number
> = {
  usagers: 0,
  professionnels: 1,
};
