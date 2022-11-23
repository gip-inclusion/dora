import { getServicesOptions } from "$lib/services";

export async function load() {
  return {
    servicesOptions: await getServicesOptions(),
  };
}
