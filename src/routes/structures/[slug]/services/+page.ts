import { getServicesOptions } from "$lib/requests/services";
import type { SERVICE_STATUSES, SERVICE_UPDATE_STATUS } from "$lib/types";
import { capitalize } from "$lib/utils/misc";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ url, parent }) => {
  const { structure } = await parent();

  const query = url.searchParams;
  const serviceStatus: SERVICE_STATUSES | undefined =
    query.get("service-status");
  const updateStatus: SERVICE_UPDATE_STATUS | undefined =
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
