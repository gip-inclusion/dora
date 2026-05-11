import type {
  AdminStructure,
  ModerationStatus,
  Service,
  Structure,
} from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import { fetchData } from "$lib/utils/misc";

export async function getStructuresAdmin(
  departmentCode
): Promise<AdminStructure[]> {
  let url = `${getApiURL()}/structures-admin/`;

  if (departmentCode) {
    url += `?department=${departmentCode}`;
  }
  return (await fetchData<AdminStructure[]>(url)).data;
}

export async function getStructureAdmin(
  slug: string,
  fetchFunction = fetch
): Promise<AdminStructure> {
  const url = `${getApiURL()}/structures-admin/${slug}/`;
  return (await fetchData<Structure>(url, fetchFunction)).data;
}

export async function getStructuresToModerate(fetchFunction = fetch) {
  const url = `${getApiURL()}/structures-admin/?moderation=1`;
  return (await fetchData(url, fetchFunction)).data;
}

export async function getServicesAdmin(fetchFunction = fetch) {
  const url = `${getApiURL()}/services-admin/`;
  return (await fetchData(url, fetchFunction)).data;
}

export async function getServiceAdmin(slug: string, fetchFunction = fetch) {
  const url = `${getApiURL()}/services-admin/${slug}/`;
  return (await fetchData<Service>(url, fetchFunction)).data;
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
    },
    body: JSON.stringify({ moderationStatus: status }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response.json();
}
