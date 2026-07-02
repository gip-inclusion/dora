import { getServicesOptions } from "$lib/requests/services";
import type { ServiceSearchResult } from "$lib/types";
import { SEARCH_KEYWORD_URL, SEARCH_RADIUS_KM } from "$lib/consts";

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
  servicesPageSize: number;
  servicesTotal: number;
  searchCenter: [number, number] | null;
  searchRadiusKm: number;
  fundingLabels: Array<{ value: string; label: string }>;
}> {
  const url = `${SEARCH_KEYWORD_URL}?${apiParams.toString()}`;

  const res = await fetchFunction(url, {
    headers: { Accept: "application/json; version=1.0" },
  });

  if (res.ok) {
    const data = await res.json();
    return data;
  }

  return {
    services: [],
    servicesPageSize: 50,
    servicesTotal: 0,
    searchCenter: null,
    searchRadiusKm: SEARCH_RADIUS_KM,
    fundingLabels: [],
  };
}

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();
  const keywords = url.searchParams.get("q");
  const {
    services,
    servicesPageSize,
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
    servicesPageSize,
    servicesTotal,
    // TODO(A/B mots-clés) : tracking dédié à la recherche par mots-clés si besoin.
    searchId: null as number | null,
  };
};
