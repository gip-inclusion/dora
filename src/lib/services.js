import insane from "insane";
import { get } from "svelte/store";

import { markdownToHTML, htmlToMarkdown, fetchData } from "$lib/utils.js";
import { getApiURL } from "$lib/utils/api.js";
import { token } from "$lib/auth";

function toBack(service) {
  if (service.fullDesc) service.fullDesc = htmlToMarkdown(service.fullDesc);
  if (service.longitude && service.latitude) {
    service.geom = {
      type: "Point",
      coordinates: [service.longitude, service.latitude],
    };
  } else {
    service.geom = null;
  }
  return service;
}

function toFront(service) {
  if (service.fullDesc)
    service.fullDesc = insane(markdownToHTML(service.fullDesc));
  let lng, lat;
  if (service.geom) {
    [lng, lat] = service.geom.coordinates;
  }
  service.longitude = lng;
  service.latitude = lat;
  return service;
}

export async function getServices() {
  const url = `${getApiURL()}/services/`;
  return (await fetchData(url)).data;
}

export async function getService(slug) {
  const url = `${getApiURL()}/services/${slug}/`;
  const data = (await fetchData(url)).data;
  if (data) return toFront(data);
  // TODO: 404
  return null;
}

export async function createOrModifyService(service) {
  let method, url;
  if (service.slug) {
    url = `${getApiURL()}/services/${service.slug}/`;
    method = "PATCH";
  } else {
    url = `${getApiURL()}/services/`;
    method = "POST";
  }

  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(toBack(service)),
  });

  const result = {
    ok: response.ok,
    status: response.status,
  };
  if (response.ok) {
    result.data = toFront(await response.json());
  } else {
    try {
      result.error = await response.json();
    } catch (err) {
      console.error(err);
    }
  }
  return result;
}

export async function publishDraft(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ isDraft: false }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return await response.json();
}

export async function unPublishDraft(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ isDraft: true }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return await response.json();
}

export async function getLastDraft() {
  if (token) {
    const url = `${getApiURL()}/services/last-draft/`;
    return (await fetchData(url)).data;
  }
  return null;
}

export async function getServicesOptions() {
  const url = `${getApiURL()}/services-options/`;
  return (await fetchData(url)).data;
}
