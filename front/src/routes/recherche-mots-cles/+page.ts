import { getServicesOptions } from "$lib/requests/services";
import type { ServiceSearchResult } from "$lib/types";
import { SEARCH_KEYWORD_URL, SEARCH_RADIUS_KM } from "$lib/consts";

import type { PageLoad } from "./$types";

// Variante A/B « recherche par mots-clés ».
async function getKeywordResults(
  apiParams: URLSearchParams,
  fetchFunction: typeof fetch
): Promise<{
  services: ServiceSearchResult[];
  servicesPages: number;
  servicesTotal: number;
  searchCenter: [number, number] | null;
  searchRadiusKm: number;
}> {
  const url = `${SEARCH_KEYWORD_URL}?${apiParams.toString()}`;

  const res = await fetchFunction(url, {
    headers: { Accept: "application/json; version=1.0" },
  });

  const data = await res.json();
  return data;
}

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();
  const keywords = url.searchParams.get("q") || "";
  let fetchError: string = "";
  let services: ServiceSearchResult[] = [];
  let servicesPages: number = 0;
  let servicesTotal: number = 0;
  let searchCenter: [number, number] | null = null;
  let searchRadiusKm = SEARCH_RADIUS_KM;
  try {
    const data = await getKeywordResults(url.searchParams, fetch);
    services = data.services;
    servicesPages = data.servicesPages;
    servicesTotal = data.servicesTotal;
    searchCenter = data.searchCenter;
    searchRadiusKm = data.searchRadiusKm;
  } catch {
    fetchError =
      "Impossible de charger les résultats, merci de réessayer ultérieurement.";
  }
  // Le tracking des PageView accepte un titre au maximum de 255 caractères.
  const titleKeywordTruncated =
    keywords.length > 30 ? `${keywords.slice(0, 30)}…` : keywords;
  return {
    title: `Recherche par mots-clés${titleKeywordTruncated ? ` : ${titleKeywordTruncated}` : ""} | DORA`,
    noIndex: true,
    keywords,
    fetchError,
    searchCenter,
    searchRadiusKm,
    services,
    servicesOptions: await getServicesOptions(fetch),
    servicesPages,
    servicesTotal,
    // TODO(A/B mots-clés) : tracking dédié à la recherche par mots-clés si besoin.
    searchId: null as number | null,
  };
};
