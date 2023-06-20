/* global plausible */
import { browser } from "$app/environment";
import { CANONICAL_URL } from "$lib/env";
import { token, userInfo } from "$lib/utils/auth";
import { getDepartmentFromCityCode } from "$lib/utils/misc";
import { get } from "svelte/store";
import { getAbTestingUserGroup } from "$lib/utils/ab-testing";

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
  };
  if (withUserData) {
    props = {
      ...props,
      loggedIn: !!get(token),
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

export function trackMobilisation(service) {
  const props = {
    ..._getServiceProps(service, true),
    abTestingGroup: getAbTestingUserGroup("mobilisation"),
  };
  _track("mobilisation", props);
  _track("mobilisation-abTesting", props);
}

export function trackMobilisationEmail(service) {
  const props = {
    ..._getServiceProps(service, true),
    abTestingGroup: getAbTestingUserGroup("mobilisation"),
  };

  _track("mobilisation-contact", props);
  _track("mobilisation-contact-abTesting", props);
}

export function trackMobilisationLogin(service) {
  const props = {
    ..._getServiceProps(service, false),
    abTestingGroup: getAbTestingUserGroup("mobilisation"),
  };

  _track("mobilisation-login", props);
  _track("mobilisation-login-abTesting", props);
}

export function trackFeedback(service) {
  _track("suggestion", _getServiceProps(service, true));
}

export function trackPDFDownload(service) {
  _track("pdf-download", _getServiceProps(service, true));
}

export function trackSearch(
  categoryIds,
  subCategoryIds,
  cityCode,
  cityLabel,
  kindIds,
  feeConditions,
  numResults
) {
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

export function trackService(service) {
  _track("service", _getServiceProps(service, true));
}

export function trackStructure(structure) {
  _track("structure", _getStructureProps(structure, true));
}
