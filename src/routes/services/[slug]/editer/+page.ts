import { browser } from "$app/environment";
import {
  getModel,
  getService,
  getServicesOptions,
} from "$lib/requests/services";
import { getStructure, getStructures } from "$lib/requests/structures";
import { userInfo } from "$lib/utils/auth";
import { error } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
  await parent();

  const user = get(userInfo);
  const service = await getService(params.slug);

  // on ne retourne une 404 que sur le client
  if (!browser) {
    return { structure: {}, structures: [], service, servicesOptions: {} };
  }

  if (!service) {
    throw error(404, "Page Not Found");
  }

  const structure = await getStructure(service.structure);
  let structures;
  if (user.isStaff) {
    structures = await getStructures();
  } else if (user) {
    structures = user.structures;
  }
  let model = null;
  if (service.model) {
    model = await getModel(service.model);
  }

  return {
    title: `Éditer | ${service.name} | ${structure.name} | DORA`,
    noIndex: true,
    service,
    servicesOptions: await getServicesOptions({ model }),
    structures,
    structure,
    model,
  };
};
