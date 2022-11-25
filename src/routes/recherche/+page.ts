import { getServicesOptions } from "$lib/services";
import {
  SERVICE_UPDATE_STATUS,
  type SearchQuery,
  type ServiceSearchResult,
} from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import { trackSearch } from "$lib/utils/plausible";
import { computeUpdateStatusData } from "$lib/utils/service";
import { getQuery } from "../_homepage/_search";

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
    return await res.json();
  }

  // TODO: log errors
  try {
    console.error(await res.json());
  } catch (err) {
    console.error(err);
  }
  return [];
}

export async function load({ url, parent }) {
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
  services.forEach((service) => {
    service.updateStatus = computeUpdateStatusData(service).updateStatus;
  });

  trackSearch(
    categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    kindIds,
    feeConditions,
    services.length
  );
  return {
    categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    kindIds,
    feeConditions,
    allServices: services,
    servicesUpToDate: services.filter(
      (service) => service.updateStatus !== SERVICE_UPDATE_STATUS.REQUIRED
    ),
    servicesToUpdate: services.filter(
      (service) => service.updateStatus === SERVICE_UPDATE_STATUS.REQUIRED
    ),
    servicesOptions: await getServicesOptions(),
  };
}
