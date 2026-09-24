import type { AdminStructure, ModerationStatus, Structure } from "$lib/types";
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

export async function setModerationState(
  entity: { slug: string },
  status: ModerationStatus
) {
  const url = `${getApiURL()}/structures-admin/${entity.slug}/`;
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
