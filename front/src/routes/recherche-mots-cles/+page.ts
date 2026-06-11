import { getKeywordResults, getServicesOptions } from "$lib/requests/services";
import type { ServiceSearchResult } from "$lib/types";
import { SEARCH_RADIUS_KM } from "$lib/consts";

import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();
  const keywords = url.searchParams.get("q") || "";
  const lon = url.searchParams.get("lon");
  const lat = url.searchParams.get("lat");
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
  const maxLength = 100;
  const titleKeywordTruncated =
    keywords.length > maxLength ? `${keywords.slice(0, maxLength)}…` : keywords;
  return {
    title: `Recherche par mots-clés${titleKeywordTruncated ? ` : ${titleKeywordTruncated}` : ""} | DORA`,
    noIndex: true,
    keywords,
    fetchError,
    lat,
    lon,
    searchCenter,
    searchRadiusKm,
    services,
    servicesOptions: await getServicesOptions(fetch),
    servicesPages,
    servicesTotal,
  };
};
