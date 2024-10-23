import { getServicesOptions } from "$lib/requests/services";
import type { ServiceStatus, ServiceUpdateStatus } from "$lib/types";
import { capitalize } from "$lib/utils/misc";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ url, parent }) => {
  const { structure } = await parent();

  const query = url.searchParams;
  const serviceStatus: ServiceStatus | undefined = query.get("service-status");
  const updateStatus: ServiceUpdateStatus | undefined =
    query.get("update-status");
  const servicesOptions = await getServicesOptions();

  return {
    title: `Services | ${capitalize(structure.name)} | DORA`,
    description: structure.shortDesc,
    serviceStatus,
    updateStatus,
    servicesOptions,
  };
};
