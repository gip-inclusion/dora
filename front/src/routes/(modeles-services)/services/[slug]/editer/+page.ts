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

  const service = await getService(params.slug, fetch);

  // on ne retourne une 404 que sur le client
  if (!browser) {
    return { structure: {}, structures: [], service, servicesOptions: {} };
  }

  if (!service) {
    error(404, "Page Not Found");
  }

  const [structure, servicesOptions, model] = await Promise.all([
    getStructure(service.structure, fetch),
    getServicesOptions(fetch),
    service.model ? getModel(service.model, fetch) : null,
  ]);

  return {
    title: `Éditer | ${service.name}${structure ? ` | ${structure.name}` : ""} | DORA`,
    noIndex: true,
    service,
    servicesOptions,
    structures: structure ? [structure] : [],
    structure,
    model,
  };
};
