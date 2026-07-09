import { getApiURL } from "$lib/utils/api";
import { getServicesOptions } from "$lib/requests/services";
import { trackKeywordSearch } from "$lib/utils/stats";
import type { ServiceSearchResult } from "$lib/types";
import { SEARCH_RADIUS_KM } from "$lib/consts";

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
  const url = `${getApiURL()}/search/keyword/}?${apiParams.toString()}`;
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
  let searchId: number | null = null;
  try {
    const data = await getKeywordResults(url.searchParams, fetch);
    services = data.services;
    servicesPages = data.servicesPages;
    servicesTotal = data.servicesTotal;
    searchCenter = data.searchCenter;
    searchRadiusKm = data.searchRadiusKm;

    // La recherche par mots-clés est paginée/filtrée côté serveur et `load` se
    // réexécute à chaque changement de page. Un `searchId` déjà présent dans
    // l'URL indique qu'on se situe dans le contexte d'une même recherche : on
    // le réutilise au lieu d'émettre un nouvel événement `search` (ce qui
    // fausserait les comptes et casserait lien à la recherche originale).
    // Sinon on émet l'évènement lors d'une nouvelle recherche (i.e. page non
    // spécifiée ou première page).
    const existingSearchId = url.searchParams.get("searchId");
    const page = url.searchParams.get("page");
    if (existingSearchId) {
      searchId = Number(existingSearchId);
    } else if (!page || page === "1") {
      const cityCode = url.searchParams.get("code_commune") ?? "";
      const categoryIds = url.searchParams.getAll("cats");
      const subCategoryIds = url.searchParams.getAll("subs");
      const kinds = url.searchParams.getAll("types");
      const feeConditions = url.searchParams.getAll("frais");
      const locationKinds = url.searchParams.getAll("modes_accueil");
      searchId = await trackKeywordSearch(
        url,
        keywords,
        cityCode,
        categoryIds,
        subCategoryIds,
        kinds,
        feeConditions,
        locationKinds,
        services,
        servicesTotal,
        fetch
      );
    }
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
    searchCenter,
    searchRadiusKm,
    services,
    servicesOptions: await getServicesOptions(fetch),
    servicesPages,
    servicesTotal,
    searchId,
  };
};
