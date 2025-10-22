import { browser } from "$app/environment";
import {
  getModel,
  getService,
  getServicesOptions,
} from "$lib/requests/services";
import { getStructure } from "$lib/requests/structures";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, params, parent }) => {
  await parent();

  const service = await getService(params.slug);

  // on ne retourne une 404 que sur le client
  if (!browser) {
    return { structure: {}, structures: [], service, servicesOptions: {} };
  }

  if (!service) {
    error(404, "Page Not Found");
  }

  const structure = await getStructure(service.structure);

  const model = service.model ? await getModel(service.model) : null;

  return {
    title: `Éditer | ${service.name} | ${structure.name} | DORA`,
    noIndex: true,
    service,
    servicesOptions: await getServicesOptions(fetch),
    structures: [structure],
    structure,
    model,
  };
};
