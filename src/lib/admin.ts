import { token } from "$lib/auth";
import type { ModerationStatus, Service, Structure } from "$lib/types";
import { fetchData } from "$lib/utils";
import { getApiURL } from "$lib/utils/api";
import { get } from "svelte/store";

export async function getStructuresAdmin() {
  const url = `${getApiURL()}/structures-admin/`;
  return (await fetchData(url)).data;
}

export async function getStructureAdmin(slug) {
  const url = `${getApiURL()}/structures-admin/${slug}/`;
  const result = (await fetchData<Structure>(url)).data;

  return result;
}

export async function getStructuresToModerate() {
  const url = `${getApiURL()}/structures-admin/?moderation=1`;
  return (await fetchData(url)).data;
}

export async function getServicesAdmin() {
  const url = `${getApiURL()}/services-admin/`;
  return (await fetchData(url)).data;
}

export async function getServiceAdmin(slug) {
  const url = `${getApiURL()}/services-admin/${slug}/`;
  return (await fetchData<Service>(url)).data;
}

export async function getServicesToModerate() {
  const url = `${getApiURL()}/services-admin/?moderation=1`;
  return (await fetchData(url)).data;
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
