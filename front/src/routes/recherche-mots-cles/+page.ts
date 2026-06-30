import { getServicesOptions } from "$lib/requests/services";
import type { ServiceSearchResult } from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import { SEARCH_RADIUS_KM } from "$lib/consts";

import type { PageLoad } from "./$types";

// Variante A/B « recherche par mots-clés ».

// TODO: On devrait pouvoir activer SSR.
// Pour des raisons de performance, les requêtes étant lourdes. Et on ne tient pas
// forcément non plus à ce qu'elles soient indexées.
export const ssr = false;

async function getKeywordResults(
  apiParams: URLSearchParams,
  fetchFunction: typeof fetch
): Promise<{
  services: ServiceSearchResult[];
  servicesTotal: number;
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
    return data;
  }

  return {
    services: [],
    servicesTotal: 0,
    searchCenter: null,
    searchRadiusKm: SEARCH_RADIUS_KM,
    fundingLabels: [],
  };
}

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();
  console.log("LOADING", url.searchParams.toString());
  const keywords = url.searchParams.get("q");
  const foo = url.searchParams.getAll("publics");
  const bar = url.searchParams.getAll("cats");
  const {
    services,
    servicesTotal,
    searchCenter,
    searchRadiusKm,
    fundingLabels,
  } = await getKeywordResults(url.searchParams, fetch);
  return {
    title: `Recherche par mots-clés${keywords ? ` : ${keywords}` : ""} | DORA`,
    noIndex: true,
    keywords,
    searchCenter,
    searchRadiusKm,
    availableFundingLabels: fundingLabels,
    services,
    servicesOptions: await getServicesOptions(fetch),
    servicesTotal,
    // TODO(A/B mots-clés) : tracking dédié à la recherche par mots-clés si besoin.
    searchId: null as number | null,
  };
};
