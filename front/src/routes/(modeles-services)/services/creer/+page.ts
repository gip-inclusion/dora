import { getNewService, toServiceStructure } from "$lib/utils/forms";
import { getModel, getServicesOptions } from "$lib/requests/services";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import { getStructure } from "$lib/requests/structures";
import type { PageLoad } from "./$types";
import type { Model, Service, ShortStructure, Structure } from "$lib/types";
import { error } from "@sveltejs/kit";

// pages authentifiées sur lesquelles la première requête non authentifiée n'a pas de sens
export const ssr = false;

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();

  const query = url.searchParams;
  const structureSlug = query.get("structure");
  const modelSlug = query.get("modele");

  const user = get(userInfo);
  if (!user) {
    return {};
  }

  const managedStructureSearchMode = user.isStaff || user.isManager;

  let structures: ShortStructure[] = user.structures;
  let service: Service;
  let model: Model | undefined = undefined;
  let structure: Structure | undefined;

  if (modelSlug) {
    model = await getModel(modelSlug, fetch);
    service = JSON.parse(JSON.stringify(model));
    service.model = modelSlug;
    service.structure = null;
    service.slug = null;
    service.locationKinds = [];
    service.isContactInfoPublic = false;
  } else {
    service = getNewService();
  }

  if (structureSlug) {
    structure = (await getStructure(structureSlug, fetch)) || undefined;
    if (structure) {
      structures = [structure];
    } else {
      error(404, "Page Not Found");
    }
  } else {
    if (managedStructureSearchMode) {
      structures = [];
    } else {
      structures = user.structures;
    }
    if (structures.length === 1) {
      // `user.structures` ne contient que des `ShortStructure` : on recharge la structure
      // complète, seule porteuse du téléphone, du courriel et des horaires.
      structure = (await getStructure(structures[0].slug, fetch)) || undefined;
    }
  }

  service.structure = structure ? structure.slug : null;

  // La structure est déjà connue ici : `handleStructureChange` ne sera jamais appelé,
  // c'est donc à nous de renseigner `structureInfo`.
  if (structure) {
    service.structureInfo = toServiceStructure(structure);
  }

  if (!model) {
    service.coachOrientationModes =
      structure && structure.noDoraForm ? [] : ["formulaire-dora"];
  }

  return {
    noIndex: true,
    title: "Création d’un service | DORA",
    servicesOptions: await getServicesOptions(fetch),
    managedStructureSearchMode,
    structures,
    structure,
    service,
    model,
  };
};
