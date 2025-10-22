import { browser } from "$app/environment";
import type { Service } from "$lib/types";
import { error } from "@sveltejs/kit";
import {
  getService,
  getServiceDI,
  getServicesOptions,
} from "$lib/requests/services";
import type { PageLoad } from "./$types";

export const ssr = false;

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
      title: `Mobiliser | ${service.name} | ${service.structureInfo.name} | DORA`,
      noIndex: true,
      service,
      isDI: true,
      servicesOptions: await getServicesOptions(fetch),
    };
  }

  const service = await getService(params.slug, fetch);

  // on ne retourne une 404 que sur le client
  if (!browser) {
    return { structures: [], service, servicesOptions: {} };
  }

  if (!service) {
    error(404, "Page Not Found");
  }

  return {
    title: `Mobiliser | ${service.name} | ${service.structureInfo.name} | DORA`,
    noIndex: true,
    service,
    servicesOptions: await getServicesOptions(fetch),
  };
};
