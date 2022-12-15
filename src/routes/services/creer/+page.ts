import { getNewService } from "$lib/utils/forms";
import {
  getLastDraft,
  getModel,
  getServicesOptions,
} from "$lib/requests/services";
import { getStructures } from "$lib/requests/structures";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

// pages authentifiées sur lesquelles la première requête non authentifiée n'a pas de sens
export const ssr = false;

export const load: PageLoad = async ({ url, parent }) => {
  await parent();

  const query = url.searchParams;
  const structureSlug = query.get("structure");
  const modelSlug = query.get("modele");

  const user = get(userInfo);
  let structures = [];

  if (user?.isStaff) {
    structures = await getStructures();
  } else if (user) {
    structures = user.structures;
  }

  let service;
  let model;

  if (modelSlug) {
    model = await getModel(modelSlug);
    service = JSON.parse(JSON.stringify(model));
    service.model = modelSlug;
    service.structure = null;
    service.slug = null;
    service.locationKinds = [];
  } else {
    service = getNewService();
  }

  let structure;

  if (structures.length === 1) {
    service.structure = structures[0].slug;
    structure = structures[0];
  } else if (structureSlug) {
    // si la structure est renseignée dans l'URL, force celle-là
    structure = structures.find((s) => s.slug === structureSlug);
    service.structure = structureSlug;
  }

  return {
    noIndex: true,
    title: "Création d'un service | DORA",
    lastDraft: await getLastDraft(),
    servicesOptions: await getServicesOptions({ model }),
    structures,
    structure,
    service,
    model,
  };
};
