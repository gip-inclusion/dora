import { getServicesOptions } from "$lib/requests/services";
import type { ServiceSearchResult } from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import { SEARCH_RADIUS_KM } from "$lib/consts";

import type { PageLoad } from "./$types";

// Variante A/B « recherche par mots-clés ».

// Pour des raisons de performance, les requêtes étant lourdes. Et on ne tient pas
// forcément non plus à ce qu'elles soient indexées.
export const ssr = false;

// TODO(A/B mots-clés) : remplacer par l'endpoint réel de recherche par mots-clés
// une fois défini côté back. En attendant, on calque sur /search/ en ajoutant le
// paramètre `q`. Le back renverra le même type `ServiceSearchResult[]`, mais trié
// par pertinence (et non par distance).
async function getKeywordResults(
  apiParams: URLSearchParams,
  fetchFunction: typeof fetch
): Promise<{
  services: ServiceSearchResult[];
  searchCenter: [number, number] | null;
  searchRadiusKm: number;
  fundingLabels: Array<{ value: string; label: string }>;
}> {
  const url = `${getApiURL()}/search/keyword/?${apiParams.toString()}`;

  const res = await fetchFunction(url, {
    headers: { Accept: "application/json; version=1.0" },
  });

  if (res.ok) {
    const data = await res.json();
    return {
      services: data.services ?? [],
      searchCenter: data.searchCenter ?? null,
      searchRadiusKm: data.searchRadiusKm ?? SEARCH_RADIUS_KM,
      fundingLabels: data.fundingLabels ?? [],
    };
  }

  return {
    services: [],
    searchCenter: null,
    searchRadiusKm: SEARCH_RADIUS_KM,
    fundingLabels: [],
  };
}

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();

  const query = url.searchParams;

  // Paramètres produits par le formulaire mots-clés
  // (service-search-keyword.svelte) : q + localisation à différents niveaux.
  const keywords = query.get("q") ?? "";
  const cityCode = query.get("code_commune") ?? undefined;
  const departmentCode = query.get("code_departement") ?? undefined;
  const regionCode = query.get("code_region") ?? undefined;
  const lon = query.get("lon");
  const lat = query.get("lat");

  // TODO(A/B mots-clés) : ajuster les noms de paramètres selon l'API définitive.
  const apiParams = new URLSearchParams();
  if (keywords) {
    apiParams.set("q", keywords);
  }
  if (cityCode) {
    apiParams.set("code_commune", cityCode);
  }
  if (departmentCode) {
    apiParams.set("code_departement", departmentCode);
  }
  if (regionCode) {
    apiParams.set("code_region", regionCode);
  }
  if (lon) {
    apiParams.set("lon", lon);
  }
  if (lat) {
    apiParams.set("lat", lat);
  }

  const { services, searchCenter, searchRadiusKm, fundingLabels } =
    await getKeywordResults(apiParams, fetch);

  return {
    title: `Recherche par mots-clés${keywords ? ` : ${keywords}` : ""} | DORA`,
    noIndex: true,
    keywords,
    cityCode,
    departmentCode,
    regionCode,
    lat,
    lon,
    searchCenter,
    searchRadiusKm,
    availableFundingLabels: fundingLabels,
    services,
    servicesOptions: await getServicesOptions(fetch),
    // TODO(A/B mots-clés) : tracking dédié à la recherche par mots-clés si besoin.
    searchId: null as number | null,
  };
};
