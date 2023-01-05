/* global plausible */
import { browser } from "$app/environment";
import { CANONICAL_URL } from "$lib/env";
import { token, userInfo } from "$lib/utils/auth";
import { getDepartmentFromCityCode } from "$lib/utils/misc";
import { get } from "svelte/store";

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
        ...(get(userInfo)?.structures.map((s) => s.slug) ?? []),
        ...(get(userInfo)?.pendingStructures.map((s) => s.slug) ?? []),
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
        ...(get(userInfo)?.structures.map((s) => s.slug) ?? []),
        ...(get(userInfo)?.pendingStructures.map((s) => s.slug) ?? []),
      ].includes(structure.slug),
    };
  }
  return props;
}

export function trackError(errorStatusCode, path) {
  _track(errorStatusCode, { path });
}

export function trackMobilisation(service) {
  _track("mobilisation", _getServiceProps(service, true));
}

export function trackMobilisationEmail(service) {
  _track("mobilisation-contact", _getServiceProps(service, true));
}

export function trackMobilisationLogin(service) {
  _track("mobilisation-login", _getServiceProps(service, false));
}

export function trackSuggestion(service) {
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
