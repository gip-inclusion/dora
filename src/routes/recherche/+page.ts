import { getServicesOptions } from "$lib/requests/services";
import type { SearchQuery, ServiceSearchResult } from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import { trackSearch } from "$lib/utils/plausible";
import { getQuery, storeLastSearchCity } from "$lib/utils/service-search";
import type { PageLoad } from "./$types";

// pour raison de performance, les requêtes étant lourdes, et on ne tient pas forcément
// à ce qu'elles soient indexées
export const ssr = false;

async function getResults({
  categoryIds,
  subCategoryIds,
  cityCode,
  cityLabel,
  kindIds,
  feeConditions,
}: SearchQuery): Promise<ServiceSearchResult[]> {
  const query = getQuery({
    categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    kindIds,
    feeConditions,
  });
  const url = `${getApiURL()}/search/?${query}`;

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

export const load: PageLoad = async ({ url, parent }) => {
  await parent();

  const query = url.searchParams;
  const categoryIds = query.get("cats") ? query.get("cats").split(",") : [];
  const subCategoryIds = query.get("subs") ? query.get("subs").split(",") : [];
  const cityCode = query.get("city");
  const cityLabel = query.get("cl");
  const kindIds = query.get("kinds") ? query.get("kinds").split(",") : [];
  const feeConditions = query.get("fees") ? query.get("fees").split(",") : [];

  const services = await getResults({
    categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    kindIds,
    feeConditions,
  });

  trackSearch(
    url,
    categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    kindIds,
    feeConditions,
    services.length
  );

  if (cityCode && cityLabel) {
    storeLastSearchCity(cityCode, cityLabel);
  }

  return {
    title: `Services d’insertion à ${cityLabel} | Recherche | DORA`,
    noIndex: true,
    categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    kindIds,
    feeConditions,
    services,
    servicesOptions: await getServicesOptions(),
  };
};
