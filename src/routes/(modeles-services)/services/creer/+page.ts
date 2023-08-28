import { getNewService } from "$lib/utils/forms";
import { getModel, getServicesOptions } from "$lib/requests/services";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import { getStructure, getManagedStructures } from "$lib/requests/structures";
import type { PageLoad } from "./$types";
import type { Model, Service, ShortStructure } from "$lib/types";
import { error } from "@sveltejs/kit";

// pages authentifiées sur lesquelles la première requête non authentifiée n'a pas de sens
export const ssr = false;

export const load: PageLoad = async ({ url, parent }) => {
  await parent();

  const query = url.searchParams;
  const structureSlug = query.get("structure");
  const modelSlug = query.get("modele");

  const user = get(userInfo);
  if (!user) {
    return {};
  }

  let structures: ShortStructure[] = user.structures;
  let service: Service;
  let model: Model | undefined = undefined;
  let structure: ShortStructure | undefined;

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

  if (structureSlug) {
    structure = structures.find((struct) => struct.slug === structureSlug);
    if (!structure && (user.isStaff || user.isManager)) {
      structure = await getStructure(structureSlug);
    }
    if (structure) {
      structures = [structure];
    } else {
      throw error(404, "Page Not Found");
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

  service.structure = structure ? structure.slug : null;

  return {
    noIndex: true,
    title: "Création d’un service | DORA",
    servicesOptions: await getServicesOptions(),
    structures,
    structure,
    service,
    model,
  };
};
