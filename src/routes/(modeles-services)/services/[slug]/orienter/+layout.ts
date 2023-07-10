import { browser } from "$app/environment";
import { error } from "@sveltejs/kit";
import { getStructure } from "$lib/requests/structures";
import { getService, getServicesOptions } from "$lib/requests/services";

export const ssr = false;

export const load = async ({ params, parent }) => {
  await parent();
  const service = await getService(params.slug);

  // on ne retourne une 404 que sur le client
  if (!browser) {
    return { structure: {}, structures: [], service, servicesOptions: {} };
  }

  if (!service) {
    throw error(404, "Page Not Found");
  }

  const structure = await getStructure(service.structure);
  return {
    title: `Mobiliser | ${service.name} | ${structure.name} | DORA`,
    noIndex: true,
    service,
    servicesOptions: await getServicesOptions(),
    structure,
  };
};
