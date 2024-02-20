import { browser } from "$app/environment";
import { token } from "$lib/utils/auth";
import { get } from "svelte/store";
import { getApiURL } from "$lib/utils/api";
import hexoid from "hexoid";

const analyticsIdKey = "userHash";

function getAnalyticsId() {
  let analyticsId = localStorage.getItem(analyticsIdKey);
  if (!analyticsId) {
    analyticsId = hexoid(32)();
    localStorage.setItem(analyticsIdKey, analyticsId);
  }
  return analyticsId;
}

async function logAnalyticsEvent(tag, path, params = {}) {
  const data = {
    tag,
    path,
    userHash: getAnalyticsId(),
    ...params,
  };
  const currentToken = get(token);

  const headers = new Headers({
    Accept: "application/json; version=1.0",
    "Content-Type": "application/json",
  });
  if (currentToken) {
    headers.append("Authorization", `Token ${currentToken}`);
  }

  const res = await fetch(`${getApiURL()}/stats/event/`, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });

  if (res.ok) {
    return res.json();
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

export function trackMobilisation(service, url, searchId) {
  if (browser) {
    logAnalyticsEvent("mobilisation", url.pathname, {
      service: service.slug,
      searchId,
    });
  }
}

export function trackDiMobilisation(service, url, searchId) {
  if (browser) {
    logAnalyticsEvent("di_mobilisation", url.pathname, {
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
  kindIds,
  feeConditions,
  results
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
    const searchId = await logAnalyticsEvent("search", url.pathname, {
      searchCityCode: cityCode,
      searchNumResults: results.length,
      categoryIds: categoryIds,
      subCategoryIds: subCategoryIds,
      numDiResults,
      numDiResultsTop10,
      resultsSlugsTop10,
    });
    return searchId;
  }
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

export function trackStructure(structure, url) {
  if (browser) {
    logAnalyticsEvent("structure", url.pathname, {
      structure: structure.slug,
    });
  }
}
