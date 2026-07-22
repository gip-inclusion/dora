import { browser } from "$app/environment";
import { getApiURL } from "$lib/utils/api";
import { hexoid } from "hexoid";
import type { Service, ServiceSearchResult, Structure } from "$lib/types";

const analyticsIdKey = "userHash";

export function getAnalyticsId() {
  if (!browser) {
    return null;
  }
  let analyticsId = localStorage.getItem(analyticsIdKey);
  if (!analyticsId) {
    analyticsId = hexoid(32)();
    localStorage.setItem(analyticsIdKey, analyticsId);
  }
  return analyticsId;
}

async function logAnalyticsEvent(
  tag,
  path,
  params = {},
  fetchFunction = fetch
) {
  const data = {
    tag,
    path,
    userHash: getAnalyticsId(),
    ...params,
  };
  const headers = new Headers({
    Accept: "application/json; version=1.0",
    "Content-Type": "application/json",
  });

  const res = await fetchFunction(`${getApiURL()}/stats/event/`, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
    keepalive: true,
  });

  if (res.ok) {
    return res.json() as Promise<{ tag: string; event: number }>;
  } else {
    try {
      console.error(await res.json());
    } catch (err) {
      console.error(err);
    }
  }
  return null;
}

export function trackPageView(pathname, title) {
  if (browser) {
    logAnalyticsEvent("pageview", pathname, {
      title: title,
    });
  }
}

type ServiceType<T extends boolean> = T extends true
  ? Pick<
      Service,
      | "structure"
      | "structureInfo"
      | "slug"
      | "name"
      | "source"
      | "categories"
      | "subcategories"
    >
  : Pick<Service, "slug">;

export async function trackMobilisation<T extends boolean>(
  service: ServiceType<T>,
  url: URL,
  isDI: T,
  searchId?: number,
  externalLink?: string
) {
  if (browser) {
    if (isDI) {
      const diService = service as ServiceType<true>;
      await logAnalyticsEvent("di_mobilisation", url.pathname, {
        diStructureId: diService.structure,
        diStructureName: diService.structureInfo.name,
        diStructureDepartment: diService.structureInfo.department,
        diServiceId: diService.slug.split("--")[1],
        diServiceName: diService.name,
        diSource: diService.source,
        diCategories: diService.categories || [],
        diSubcategories: diService.subcategories || [],
        searchId: searchId || url.searchParams.get("searchId"),
        externalLink,
      });
    } else {
      const doraService = service as ServiceType<false>;
      await logAnalyticsEvent("mobilisation", url.pathname, {
        service: doraService.slug,
        searchId: searchId || url.searchParams.get("searchId"),
        externalLink,
      });
    }
  }
}

export function trackOrientation(orientation, url) {
  if (browser) {
    logAnalyticsEvent("orientation", url.pathname, {
      orientation: orientation.id,
      diStructureName: orientation.diStructureName,
      diServiceId: orientation.diServiceId,
      diServiceName: orientation.diServiceName,
    });
  }
}

export async function trackSearch(
  url,
  categoryIds,
  subCategoryIds,
  cityCode,
  cityLabel,
  kinds,
  feeConditions,
  locationKinds,
  fundingLabels,
  results,
  fetchFunction = fetch
) {
  if (browser) {
    const numResults = results.length;
    const numDiResults = results.filter(
      (service) => service.type === "di"
    ).length;
    const numDiResultsTop10 = results
      .slice(0, 10)
      .filter((service) => service.type === "di").length;
    const resultsSlugsTop10 = results
      .slice(0, 10)
      .map((service) => service.slug);

    const event = await logAnalyticsEvent(
      "search",
      url.pathname,
      {
        searchType: "thematique",
        searchCityCode: cityCode,
        searchNumResults: numResults,
        categoryIds: categoryIds,
        subCategoryIds: subCategoryIds,
        numDiResults,
        numDiResultsTop10,
        resultsSlugsTop10,
        kinds,
        feeConditions,
        locationKinds,
        fundingLabels,
      },
      fetchFunction
    );
    const searchId = event && event.event;
    return searchId;
  }
  return null;
}

// Variante A/B « recherche par mots-clés » : même événement `search` que la
// recherche thématique mais auquel on rajoute (1) `searchType` pour les
// distinguer et (2) `keyword` qui contiendra le texte recherché.
// Contrairement à `trackSearch`, il n'y a pas de `fundingLabels`, et
// `numResults` correspond au nombre total de résultats (selon le serveur)
// et non à la seule page courante.
export async function trackKeywordSearch(
  url: URL,
  keyword: string,
  cityCode: string,
  categoryIds: string[],
  subCategoryIds: string[],
  kinds: string[],
  feeConditions: string[],
  locationKinds: string[],
  results: ServiceSearchResult[],
  numResults: number,
  fetchFunction = fetch
) {
  if (!browser) {
    return null;
  }
  // Seulement sur la première page (max 50 résultats). Ce chiffre n’est pas
  // comparable avec la recherche historique, qui n’est pas paginée.
  const numDiResults = results.filter(
    (service) => service.type === "di"
  ).length;
  const numDiResultsTop10 = results
    .slice(0, 10)
    .filter((service) => service.type === "di").length;
  const resultsSlugsTop10 = results.slice(0, 10).map((service) => service.slug);

  const event = await logAnalyticsEvent(
    "search",
    url.pathname,
    {
      searchType: "mots_cles",
      keyword,
      searchCityCode: cityCode,
      searchNumResults: numResults,
      categoryIds,
      subCategoryIds,
      numDiResults,
      numDiResultsTop10,
      resultsSlugsTop10,
      kinds,
      feeConditions,
      locationKinds,
    },
    fetchFunction
  );
  const searchId = event && event.event;
  return searchId;
}

export function trackService(service, url, searchId, isDI) {
  if (browser) {
    if (isDI) {
      logAnalyticsEvent("di_service", url.pathname, {
        diStructureId: service.structure,
        diStructureName: service.structureInfo.name,
        diStructureDepartment: service.structureInfo.department,
        diServiceId: service.slug.split("--")[1],
        diServiceName: service.name,
        diSource: service.source,
        diCategories: service.categories || [],
        diSubcategories: service.subcategories || [],
        searchId,
      });
    } else {
      logAnalyticsEvent("service", url.pathname, {
        service: service.slug,
        searchId,
      });
    }
  }
}

export function trackStructure(
  structure: Structure,
  url: URL,
  fetchFunction = fetch
) {
  if (browser) {
    logAnalyticsEvent(
      "structure",
      url.pathname,
      {
        structure: structure.slug,
        searchId: url.searchParams.get("searchId"),
      },
      fetchFunction
    );
  }
}

export function trackStructureInfos(structure: Structure, url) {
  if (browser) {
    logAnalyticsEvent("structure_infos", url.pathname, {
      structure: structure.slug,
    });
  }
}
