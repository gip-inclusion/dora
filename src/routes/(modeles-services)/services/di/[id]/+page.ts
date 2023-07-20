import { getServiceDI, getServicesOptions } from "$lib/requests/services";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";
import type { Service } from "$lib/types";

export const load: PageLoad = async ({ params, parent }) => {
  await parent();

  const service = (await getServiceDI(params.id)) as Service;

  if (!service) {
    throw error(404, "Page Not Found");
  }

  return {
    title: `${service.name} | ${service.structureInfo.name} | DORA`,
    description: service.shortDesc,
    service,
    servicesOptions: await getServicesOptions(),
  };
};
