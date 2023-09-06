/* global plausible */
import { browser } from "$app/environment";
import { CANONICAL_URL } from "$lib/env";
import { token, userInfo } from "$lib/utils/auth";
import { getDepartmentFromCityCode } from "$lib/utils/misc";
import { get } from "svelte/store";
import { logAnalyticsEvent } from "$lib/utils/stats";

function _track(tag, props) {
  if (browser) {
    plausible(tag, {
      props,
    });
  }
}

function _getServiceProps(service, withUserData = false) {
  let props = {
    service: service.name,
    slug: service.slug,
    structure: service.structureInfo.name,
    departement: service.department || service.structureInfo.department,
    department: service.department || service.structureInfo.department,
    perimeter: service.diffusionZoneType,
    url: `${CANONICAL_URL}/services/${service.slug}`,
    orientable: service.isOrientable,
  };
  if (withUserData) {
    props = {
      ...props,
      loggedIn: !!get(token),
      profile: get(userInfo)?.mainActivity,
      owner: [
        ...(get(userInfo)?.structures.map((struct) => struct.slug) ?? []),
        ...(get(userInfo)?.pendingStructures.map((struct) => struct.slug) ??
          []),
      ].includes(service.structureInfo.slug),
    };
  }
  return props;
}

function _getStructureProps(structure, withUserData = false) {
  let props = {
    structure: structure.name,
    slug: structure.slug,
    departement: structure.department,
    department: structure.department,
    url: `${CANONICAL_URL}/structures/${structure.slug}`,
  };
  if (withUserData) {
    props = {
      ...props,
      loggedIn: !!get(token),
      profile: get(userInfo)?.mainActivity,
      owner: [
        ...(get(userInfo)?.structures.map((struct) => struct.slug) ?? []),
        ...(get(userInfo)?.pendingStructures.map((struct) => struct.slug) ??
          []),
      ].includes(structure.slug),
    };
  }
  return props;
}

export function trackError(errorStatusCode, path) {
  _track(errorStatusCode, { path });
}

export function trackMobilisation(service, url) {
  if (browser) {
    logAnalyticsEvent("mobilisation", url.pathname, {
      service: service.slug,
    });
  }
  _track("mobilisation", _getServiceProps(service, true));
}

export function trackDiMobilisation(service, url) {
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
    });
  }
}
export function trackOrientation(orientation, url) {
  if (browser) {
    logAnalyticsEvent("orientation", url.pathname, {
      orientation: orientation.id,
    });
  }
}

export function trackMobilisationEmail(service) {
  _track("mobilisation-contact", _getServiceProps(service, true));
}

export function trackMobilisationLogin(service) {
  _track("mobilisation-login", _getServiceProps(service, false));
}

export function trackFeedback(service) {
  _track("suggestion", _getServiceProps(service, true));
}

export function trackPDFDownload(service) {
  _track("pdf-download", _getServiceProps(service, true));
}

export function trackSearch(
  url,
  categoryIds,
  subCategoryIds,
  cityCode,
  cityLabel,
  kindIds,
  feeConditions,
  results
) {
  const numResults = results.length;

  if (browser) {
    const numDiResults = results.filter(
      (service) => service.type === "di"
    ).length;
    const numDiResultsTop10 = results
      .slice(0, 10)
      .filter((service) => service.type === "di").length;
    logAnalyticsEvent("search", url.pathname, {
      searchCityCode: cityCode,
      searchNumResults: results.length,
      categoryIds: categoryIds,
      subCategoryIds: subCategoryIds,
      numDiResults,
      numDiResultsTop10,
    });
  }

  let numResultsCat;
  if (numResults === 0) {
    numResultsCat = "0";
  } else if (numResults <= 5) {
    numResultsCat = "Entre 1 et 5";
  } else {
    numResultsCat = "Plus de 5";
  }
  _track("recherche", {
    categoryIds: categoryIds.join(","),
    subCategoryIds: subCategoryIds.join(","),
    cityCode,
    cityLabel,
    serviceKinds: kindIds.join(","),
    feeConditions: feeConditions.join(","),
    loggedIn: !!get(token),
    profile: get(userInfo)?.mainActivity,
    numResults: numResultsCat,
    department: getDepartmentFromCityCode(cityCode),
  });
}

export function trackJoinStructure() {
  _track("inscription", { step: "Adhésion structure" });
}

export function trackModel(model) {
  const props = _getServiceProps(model, true);
  props.model = props.structure;
  delete props.model;
  _track("modele", props);
}

export function trackService(service, url) {
  if (browser) {
    logAnalyticsEvent("service", url.pathname, {
      service: service.slug,
    });

    if (get(token) && service.isOrientable) {
      _track("service-orientable", _getServiceProps(service, true));
    }
  }

  _track("service", _getServiceProps(service, false));
}

export function trackDIService(service, url) {
  if (browser) {
    logAnalyticsEvent("di_service", url.pathname, {
      diStructureId: service.structure,
      diStructureName: service.structureInfo.name,
      diStructureDepartment: service.structureInfo.department,
      diServiceId: service.slug.split("--")[1],
      diServiceName: service.name,
      diSource: service.source,
      diCategories: service.categories || [],
      diSubcategories: service.subcategories || [],
    });
  }
}

export function trackStructure(structure, url) {
  if (browser) {
    logAnalyticsEvent("structure", url.pathname, {
      structure: structure.slug,
    });
  }
  _track("structure", _getStructureProps(structure, true));
}
