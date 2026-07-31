import { browser } from "$app/environment";
import {
  getService,
  getServiceDI,
  getServicesOptions,
} from "$lib/requests/services";
import type { Service } from "$lib/types";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, params, parent }) => {
  await parent();

  if (params.slug.startsWith("di--")) {
    const service = (await getServiceDI(
      params.slug.slice(4),
      fetch
    )) as Service;
    if (!service) {
      error(404, "Page Not Found");
    }

    return {
      title: `${service.name} | ${service.structureInfo.name} | DORA`,
      description: service.shortDesc,
      service,
      servicesOptions: await getServicesOptions(fetch),
      isDI: true,
      noIndex: true,
    };
  }

  const service = await getService(params.slug, fetch);
  // si le service est en brouillon il faut un token pour y accéder
  // on renvoie donc un objet vide côté serveur
  if (!service) {
    if (!browser) {
      return {
        service: null,
      };
    }
    error(404, "Page Not Found");
  }

  return {
    title: `${service.name} | ${service.structureInfo.name} | DORA`,
    description: service.shortDesc,
    service,
    servicesOptions: await getServicesOptions(fetch),
  };
};
