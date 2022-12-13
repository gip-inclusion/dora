import { browser } from "$app/environment";
import { getCityLabel } from "$lib/geo";
import { getLastSearchCity } from "$lib/search";
import { getServicesOptions } from "$lib/services";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent, url }) => {
  await parent();
  const query = url.searchParams;

  let cityCode = query.get("city");
  let cityLabel: string;

  if (cityCode) {
    cityLabel = await getCityLabel(cityCode);
  } else if (browser) {
    ({ cityCode, cityLabel } = getLastSearchCity());
  }

  return {
    title: "DORA : recensement et mise à jour de l’offre d’insertion",
    description:
      "Le service public numérique de recensement et mise à jour de l’offre d’insertion.",
    servicesOptions: await getServicesOptions(),
    cityCode,
    cityLabel,
  };
};
