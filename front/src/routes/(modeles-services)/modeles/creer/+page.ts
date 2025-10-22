import { createModelFromService, getNewModel } from "$lib/utils/forms";
import { getService, getServicesOptions } from "$lib/requests/services";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import { getStructure, getManagedStructures } from "$lib/requests/structures";
import type { PageLoad } from "./$types";
import type { Model, ShortStructure } from "$lib/types";
import { error } from "@sveltejs/kit";

// pages authentifiées sur lesquelles la première requête non authentifiée n'a pas de sens
export const ssr = false;

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();

  const serviceSlug = url.searchParams.get("service");
  const structureSlug = url.searchParams.get("structure");

  const user = get(userInfo);
  let structures: ShortStructure[] = user.structures;
  let model: Model;
  let structure: ShortStructure | undefined;

  if (serviceSlug) {
    const service = await getService(serviceSlug);
    model = createModelFromService(service);
    model.slug = null;
    model.structure = null;
    model.service = serviceSlug;
  } else {
    model = getNewModel();
  }

  if (structureSlug) {
    structure = structures.find((struct) => struct.slug === structureSlug);
    if (!structure && (user.isStaff || user.isManager)) {
      structure = await getStructure(structureSlug);
    }
    if (structure) {
      structures = [structure];
    } else {
      error(404, "Page Not Found");
    }
  } else {
    if (user.isStaff || user.isManager) {
      structures = await getManagedStructures();
    } else {
      structures = user.structures;
    }
    if (structures.length === 1) {
      structure = structures[0];
    }
  }

  model.structure = structure ? structure.slug : null;

  return {
    title: "Création d’un modèle | DORA",
    noIndex: true,
    model,
    servicesOptions: await getServicesOptions(fetch),
    structures,
    structure,
    serviceSlug,
  };
};
