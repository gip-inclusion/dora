import { getServicesOptions } from "$lib/services";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
  await parent();
  return {
    title: "DORA : recensement et mise à jour de l’offre d’insertion",
    description:
      "Le service public numérique de recensement et mise à jour de l’offre d’insertion.",
    servicesOptions: await getServicesOptions(),
  };
};
