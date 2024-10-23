import type {
  AdminShortStructure,
  ModerationStatus,
  Service,
  Structure,
} from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import { token } from "$lib/utils/auth";
import { logException } from "$lib/utils/logger";
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

export async function getStructureAdmin(slug): Promise<AdminShortStructure> {
  const url = `${getApiURL()}/structures-admin/${slug}/`;
  return (await fetchData<Structure>(url)).data;
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

export async function getServiceSuggestions() {
  const url = `${getApiURL()}/services-suggestions/`;
  const results = (await fetchData(url)).data;
  if (!results) {
    return [];
  }

  return results;
}

export async function deleteServiceSuggestion(suggestion) {
  const url = `${getApiURL()}/services-suggestions/${suggestion.id}/`;
  const method = "DELETE";
  const res = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      Authorization: `Token ${get(token)}`,
    },
  });

  const result = {
    ok: res.ok,
    status: res.status,
  };
  if (!res.ok) {
    try {
      result.error = await res.json();
    } catch (err) {
      logException(err);
    }
  }
  return result;
}

export async function acceptServiceSuggestion(suggestion) {
  const url = `${getApiURL()}/services-suggestions/${suggestion.id}/validate/`;
  const method = "POST";
  const res = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      Authorization: `Token ${get(token)}`,
    },
  });

  const result = {
    ok: res.ok,
    status: res.status,
  };

  if (!res.ok) {
    try {
      result.error = await res.json();
    } catch (err) {
      logException(err);
    }
  } else {
    try {
      result.data = await res.json();
    } catch (err) {
      logException(err);
    }
  }
  return result;
}

export function publishServiceSuggestion(suggestion, source) {
  const url = `${getApiURL()}/services-suggestions/`;
  const method = "POST";
  const { siret, name, ...contents } = suggestion;
  const authToken = get(token);
  return fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: authToken ? `Token ${get(token)}` : undefined,
    },
    body: JSON.stringify({
      siret,
      name,
      contents,
      source,
    }),
  });
}
