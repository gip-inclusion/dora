import { goto } from "$app/navigation";
import { get } from "svelte/store";
import { orientation as orientationStore } from "../store";
import { orientationStep1Schema } from "../schema";
import {
  computeConcernedPublicChoices,
  computeRequirementsChoices,
} from "$lib/utils/orientation";
import { validate } from "$lib/validation/validation";

export const load = async ({ parent }) => {
  const data = await parent();
  const { service, servicesOptions, isDI } = data;

  const orientation = get(orientationStore);
  if (!orientation.firstStepDone) {
    goto(`/services/${isDI ? "di--" : ""}${service.slug}/orienter`);
    return {};
  }

  // Pour gérer le retour arrière du navigateur permettant d'ignorer la validation,
  // on valide à nouveau le formulaire ici
  const { concernedPublicRequired } = computeConcernedPublicChoices(service);
  orientationStep1Schema.situation.required = concernedPublicRequired;

  const { requirementRequired } = computeRequirementsChoices(service);
  orientationStep1Schema.requirements.required = requirementRequired;

  const isValid = validate(orientation, orientationStep1Schema, {
    noScroll: true,
    showErrors: false,
    servicesOptions,
  }).valid;

  if (!isValid) {
    goto(`/services/${isDI ? "di--" : ""}${service.slug}/orienter`);
    return {};
  }

  return {
    ...data,
  };
};
