import { getServicesOptions } from "$lib/requests/services";
import type { SearchQuery, ServiceSearchResult } from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import { trackSearch } from "$lib/utils/stats";
import { getQueryString, storeLastSearchCity } from "$lib/utils/service-search";
import type { PageLoad } from "./$types";

// pour raison de performance, les requêtes étant lourdes, et on ne tient pas forcément
// à ce qu'elles soient indexées
export const ssr = false;

async function getResults(
  {
    categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    label,
    kindIds,
    feeConditions,
    locationKinds,
    fundingLabels,
    lat,
    lon,
  }: SearchQuery,
  fetch = window.fetch
): Promise<{
  cityBounds: [number, number, number, number];
  fundingLabels: Array<{ value: string; label: string }>;
  services: ServiceSearchResult[];
}> {
  const querystring = getQueryString({
    categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    label,
    kindIds,
    feeConditions,
    locationKinds,
    fundingLabels,
    lat,
    lon,
  });
  const url = `${getApiURL()}/search/?${querystring}`;

  const res = await fetch(url, {
    headers: { Accept: "application/json; version=1.0" },
  });

  if (res.ok) {
    return res.json();
  }

  // TODO: log errors
  try {
    console.error(await res.json());
  } catch (err) {
    console.error(err);
  }
  return [];
}

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();

  const query = url.searchParams;

  let categoryIds = query.get("cats") ? query.get("cats").split(",") : [];
  const subCategoryIds = query.get("subs") ? query.get("subs").split(",") : [];
  const cityCode = query.get("city");
  const cityLabel = query.get("cl");
  const label = query.get("l") || cityLabel;
  const kindIds = query.get("kinds") ? query.get("kinds").split(",") : [];
  const feeConditions = query.get("fees") ? query.get("fees").split(",") : [];
  const locationKinds = query.get("locs") ? query.get("locs").split(",") : [];
  const fundingLabels = query.get("funding")
    ? query.get("funding").split(",")
    : [];
  const lon = query.get("lon");
  const lat = query.get("lat");

  const {
    cityBounds,
    fundingLabels: availableFundingLabels,
    services,
  } = await getResults(
    {
      // La priorité est donnée aux sous-catégories
      categoryIds: subCategoryIds.length ? [] : categoryIds,
      subCategoryIds,
      cityCode,
      cityLabel,
      label,
      // Le filtrage sur kindIds, feeConditions et locationKinds se fait côté frontend
      kindIds: [],
      feeConditions: [],
      locationKinds: [],
      fundingLabels: [],
      lon,
      lat,
    },
    fetch
  );

  const searchId = await trackSearch(
    url,
    // La priorité est donnée aux sous-catégories
    subCategoryIds.length ? [] : categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    kindIds,
    feeConditions,
    locationKinds,
    fundingLabels,
    services
  );

  if (cityCode && cityLabel) {
    storeLastSearchCity(cityCode, cityLabel);
  }

  // Pour le formulaire de recherche, on veut afficher la catégorie sélectionnée
  if (subCategoryIds.length && !categoryIds.length) {
    categoryIds = [subCategoryIds[0].split("--")[0]];
  }

  return {
    title: `Services d’insertion à ${label} | Recherche | DORA`,
    noIndex: true,
    categoryIds,
    subCategoryIds,
    cityBounds,
    cityCode,
    cityLabel,
    label,
    lat,
    lon,
    kindIds,
    feeConditions,
    locationKinds,
    fundingLabels,
    availableFundingLabels,
    services,
    servicesOptions: await getServicesOptions(fetch),
    searchId,
  };
};
