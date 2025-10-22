import { browser } from "$app/environment";
import { getCityLabel } from "$lib/requests/geo";
import { getServicesOptions } from "$lib/requests/services";
import { getLastSearchCity } from "$lib/utils/service-search";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, parent, url, data }) => {
  await parent();
  const query = url.searchParams;

  let cityCode = query.get("city");
  let cityLabel: string | null | undefined;

  if (cityCode) {
    cityLabel = await getCityLabel(cityCode, fetch);
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
    ...data,
  };
};
