import { getServicesOptions } from "$lib/services";

export async function load({ url }) {
  const query = url.searchParams;
  return {
    serviceStatus: query.get("service-status"),
    updateStatus: query.get("update-status"),
    servicesOptions: await getServicesOptions(),
  };
}
