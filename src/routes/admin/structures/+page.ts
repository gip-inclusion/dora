import { getServicesOptions } from "$lib/requests/services";
import { getStructuresOptions } from "$lib/requests/structures";
import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  const [servicesOptions, structuresOptions] = await Promise.all([
    getServicesOptions(),
    getStructuresOptions(),
  ]);

  return {
    title: "Structures | Administration | DORA",
    noIndex: true,
    servicesOptions,
    structuresOptions,
  };
};
