import { toast } from "@zerodevx/svelte-toast";
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
  fetchFunction: typeof fetch
): Promise<{
  cityBounds: [number, number, number, number];
  fundingLabels: Array<{ value: string; label: string }>;
  services: ServiceSearchResult[];
  wrongCategoriesOrSubcategories?: boolean;
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

  const res = await fetchFunction(url, {
    headers: { Accept: "application/json; version=1.0" },
  });

  if (res.ok) {
    return res.json();
  }

  if (res.status === 400) {
    const errors = await res.json();
    const error = errors[0];
    if (error?.code === "invalid_categories_or_subcategories") {
      toast.push(
        "Les thématiques et besoins sélectionnés sont invalides. Veuillez les corriger."
      );
      return {
        cityBounds: [0, 0, 0, 0],
        fundingLabels: [],
        services: [],
        wrongCategoriesOrSubcategories: true,
      };
    }
  }

  return {
    cityBounds: [0, 0, 0, 0],
    fundingLabels: [],
    services: [],
  };
}

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();

  const query = url.searchParams;

  let categoryIds = query.get("cats")?.split(",") ?? [];
  let subCategoryIds = query.get("subs")?.split(",") ?? [];
  const cityCode = query.get("city") ?? undefined;
  const cityLabel = query.get("cl") ?? undefined;
  const label = query.get("l") ?? cityLabel;
  const kindIds = query.get("kinds")?.split(",") ?? [];
  const feeConditions = query.get("fees")?.split(",") ?? [];
  const locationKinds = query.get("locs")?.split(",") ?? [];
  const fundingLabels = query.get("funding")?.split(",") ?? [];
  const lon = query.get("lon");
  const lat = query.get("lat");

  const {
    cityBounds,
    fundingLabels: availableFundingLabels,
    services,
    wrongCategoriesOrSubcategories,
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

  if (wrongCategoriesOrSubcategories) {
    categoryIds = [];
    subCategoryIds = [];
  }

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
    services,
    fetch
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
