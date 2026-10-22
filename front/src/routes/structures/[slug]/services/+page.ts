import { getServicesOptions } from "#lib/requests/services.js";
import type { ServiceStatus } from "#lib/types.js";
import { capitalize } from "#lib/utils/misc.js";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, url, parent }) => {
  const { structure } = await parent();

  const query = url.searchParams;
  const serviceStatus: ServiceStatus | null = query.get(
    "service-status"
  ) as ServiceStatus | null;
  const updateNeeded: "true" | "false" | null = query.get("update-needed") as
    "true" | "false" | null;
  const servicesOptions = await getServicesOptions(fetch);

  return {
    title: `Services | ${capitalize(structure.name)} | DORA`,
    description: structure.shortDescription,
    serviceStatus,
    updateNeeded,
    servicesOptions,
  };
};
