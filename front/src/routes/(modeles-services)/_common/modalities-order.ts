import type { BeneficiaryAccessModes, CoachOrientationModes } from "$lib/types";

export const orderedCoachOrientationModeValues: Record<
  CoachOrientationModes,
  number
> = {
  "formulaire-dora": 0,
  "completer-le-formulaire-dadhesion": 1,
  "envoyer-un-mail-avec-une-fiche-de-prescription": 2,
  "envoyer-un-mail": 3,
  telephoner: 4,
  autre: 5,
};

export const orderedBeneficiariesAccessModeValues: Record<
  BeneficiaryAccessModes,
  number
> = {
  professionnel: 0,
  "se-presenter": 1,
  "completer-le-formulaire-dadhesion": 2,
  "envoyer-un-mail": 3,
  telephoner: 4,
  autre: 5,
};
