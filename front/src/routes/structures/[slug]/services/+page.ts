import { getServicesOptions } from "$lib/requests/services";
import type { ServiceStatus } from "$lib/types";
import { capitalize } from "$lib/utils/misc";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, url, parent }) => {
  const { structure } = await parent();

  const query = url.searchParams;
  const serviceStatus: ServiceStatus | null = query.get(
    "service-status"
  ) as ServiceStatus | null;
  const updateNeeded: "true" | "false" | null = query.get("update-needed") as
    | "true"
    | "false"
    | null;
  const servicesOptions = await getServicesOptions(fetch);

  return {
    title: `Services | ${capitalize(structure.name)} | DORA`,
    description: structure.shortDesc,
    serviceStatus,
    updateNeeded,
    servicesOptions,
  };
};
