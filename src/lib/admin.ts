import { get } from "svelte/store";

import { token } from "$lib/auth";
import { fetchData } from "$lib/utils.js";
import { getApiURL } from "$lib/utils/api.js";
import type { ModerationStatus } from "$lib/enums";

export async function getStructuresAdmin({ kitFetch } = {}) {
  const url = `${getApiURL()}/structures-admin/`;
  return (await fetchData(url, { kitFetch })).data;
}

export async function getStructureAdmin(slug, { kitFetch } = {}) {
  const url = `${getApiURL()}/structures-admin/${slug}/`;
  const result = (await fetchData(url, { kitFetch })).data;

  return result;
}

export async function getStructuresToModerate({ kitFetch } = {}) {
  const url = `${getApiURL()}/structures-admin/?moderation=1`;
  return (await fetchData(url, { kitFetch })).data;
}

export async function getServicesAdmin({ kitFetch } = {}) {
  const url = `${getApiURL()}/services-admin/`;
  return (await fetchData(url, { kitFetch })).data;
}

export async function getServiceAdmin(slug, { kitFetch } = {}) {
  const url = `${getApiURL()}/services-admin/${slug}/`;
  return (await fetchData(url, { kitFetch })).data;
}

export async function getServicesToModerate({ kitFetch } = {}) {
  const url = `${getApiURL()}/services-admin/?moderation=1`;
  return (await fetchData(url, { kitFetch })).data;
}

export async function setModerationState(entity, status: ModerationStatus) {
  const urlFragment = entity.services ? "structures-admin" : "services-admin";
  const url = `${getApiURL()}/${urlFragment}/${entity.slug}/`;
  const method = "PATCH";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ moderationStatus: status }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return await response.json();
}
