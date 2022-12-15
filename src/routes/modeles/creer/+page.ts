import { createModelFromService, getNewModel } from "$lib/utils/forms";
import { getService, getServicesOptions } from "$lib/requests/services";
import { getStructures } from "$lib/requests/structures";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

// pages authentifiées sur lesquelles la première requête non authentifiée n'a pas de sens
export const ssr = false;

export const load: PageLoad = async ({ url, parent }) => {
  await parent();

  const serviceSlug = url.searchParams.get("service");
  const structureSlug = url.searchParams.get("structure");

  const user = get(userInfo);
  let structures = [];

  if (user?.isStaff) {
    structures = await getStructures();
  } else if (user) {
    structures = user.structures;
  }

  let model;

  if (serviceSlug) {
    const service = await getService(serviceSlug);
    model = createModelFromService(service);
    model.slug = null;
    model.structure = null;
    model.service = serviceSlug;
  } else {
    model = getNewModel();
  }

  let structure;

  if (structures.length === 1) {
    model.structure = structures[0].slug;
    structure = structures[0];
  } else if (structureSlug) {
    structure = structures.find((s) => s.slug === structureSlug);
    model.structure = structureSlug;
  }

  return {
    title: "Création d’un modèle | DORA",
    noIndex: true,
    model,
    servicesOptions: await getServicesOptions({ model }),
    structures,
    structure,
    serviceSlug,
  };
};
