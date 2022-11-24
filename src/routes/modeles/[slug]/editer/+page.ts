import { error } from "@sveltejs/kit";
import { get } from "svelte/store";
import { browser } from "$app/environment";

import { userInfo } from "$lib/auth";
import { getServicesOptions, getModel } from "$lib/services";
import { getStructure, getStructures } from "$lib/structures";

export async function load({ params, parent }) {
  await parent();

  const user = get(userInfo);
  const model = await getModel(params.slug);
  let structure = {};
  let structures = [];
  const servicesOptions = await getServicesOptions({ model });

  // on ne retourne une 404 que sur le client
  if (!browser) {
    return { structure, structures, model, servicesOptions };
  }

  if (!model) {
    throw error(404, "Page Not Found");
  }

  structure = await getStructure(model.structure);

  if (user.isStaff) {
    structures = await getStructures();
  } else if (user) {
    structures = user.structures;
  }

  return {
    model,
    servicesOptions,
    structures,
    structure,
  };
}
