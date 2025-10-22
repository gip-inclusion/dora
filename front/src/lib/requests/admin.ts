import type {
  AdminShortStructure,
  ModerationStatus,
  Service,
  Structure,
} from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import { token } from "$lib/utils/auth";
import { fetchData } from "$lib/utils/misc";
import { get } from "svelte/store";

export async function getStructuresAdmin(
  departmentCode
): Promise<AdminShortStructure[]> {
  let url = `${getApiURL()}/structures-admin/`;

  if (departmentCode) {
    url += `?department=${departmentCode}`;
  }
  return (await fetchData<AdminShortStructure[]>(url)).data;
}

export async function getStructureAdmin(
  slug: string,
  fetch = window.fetch
): Promise<AdminShortStructure> {
  const url = `${getApiURL()}/structures-admin/${slug}/`;
  return (await fetchData<Structure>(url, fetch)).data;
}

export async function getStructuresToModerate() {
  const url = `${getApiURL()}/structures-admin/?moderation=1`;
  return (await fetchData(url)).data;
}

export async function getServicesAdmin() {
  const url = `${getApiURL()}/services-admin/`;
  return (await fetchData(url)).data;
}

export async function getServiceAdmin(slug: string, fetch = window.fetch) {
  const url = `${getApiURL()}/services-admin/${slug}/`;
  return (await fetchData<Service>(url, fetch)).data;
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
  return response.json();
}
