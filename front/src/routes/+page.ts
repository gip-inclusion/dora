import { browser } from "$app/env";
import { getCityLabel } from "#lib/requests/geo.ts";
import { getServicesOptions } from "#lib/requests/services.ts";
import { getLastSearchLocation } from "#lib/utils/service-search.ts";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, parent, url, data }) => {
  await parent();
  const query = url.searchParams;

  let cityCode = query.get("city");
  let cityLabel: string | null | undefined;
  let label: string | undefined;
  let lon: number | undefined;
  let lat: number | undefined;

  if (cityCode) {
    cityLabel = await getCityLabel(cityCode, fetch);
  } else if (browser) {
    const lastLocation = getLastSearchLocation();
    cityCode = lastLocation.cityCode ?? null;
    ({ cityLabel, label } = lastLocation);
    if (lastLocation.lon && lastLocation.lat) {
      lon = Number(lastLocation.lon);
      lat = Number(lastLocation.lat);
    }
  }

  return {
    title: "DORA : recensement et mise à jour de l’offre d’insertion",
    description:
      "Le service public numérique de recensement et mise à jour de l’offre d’insertion.",
    servicesOptions: await getServicesOptions(fetch),
    cityCode,
    cityLabel,
    label: label ?? cityLabel,
    lon,
    lat,
    ...data,
  };
};
