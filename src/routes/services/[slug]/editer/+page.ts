import { error } from "@sveltejs/kit";
import { get } from "svelte/store";
import { browser } from "$app/environment";

import { userInfo } from "$lib/auth";
import { getServicesOptions, getService, getModel } from "$lib/services";
import { getStructure, getStructures } from "$lib/structures";

export async function load({ params, parent }) {
  await parent();

  const user = get(userInfo);
  const service = await getService(params.slug);
  let structure = {};
  let structures = [];
  let model = null;

  // on ne retourne une 404 que sur le client
  if (!browser) {
    return { structure, structures, service, servicesOptions: {} };
  }

  if (!service) {
    throw error(404, "Page Not Found");
  }

  structure = await getStructure(service.structure);

  if (user.isStaff) {
    structures = await getStructures();
  } else if (user) {
    structures = user.structures;
  }

  if (service.model) {
    model = await getModel(service.model);
  }

  return {
    service,
    servicesOptions: await getServicesOptions({ model }),
    structures,
    structure,
    model,
  };
}
