import { getServicesOptions } from "$lib/services";
import type { SERVICE_STATUSES, SERVICE_UPDATE_STATUS } from "$lib/types";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ url, parent }) => {
  await parent();

  const query = url.searchParams;
  const serviceStatus: SERVICE_STATUSES | undefined =
    query.get("service-status");
  const updateStatus: SERVICE_UPDATE_STATUS | undefined =
    query.get("update-status");
  const servicesOptions = await getServicesOptions();

  return {
    serviceStatus,
    updateStatus,
    servicesOptions,
  };
};
