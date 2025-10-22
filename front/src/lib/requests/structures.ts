import { getApiURL } from "$lib/utils/api";
import { token } from "$lib/utils/auth";
import { fetchData } from "$lib/utils/misc";
import { get } from "svelte/store";
import type {
  PutativeStructureMember,
  ShortStructure,
  Structure,
  StructureMember,
  StructuresOptions,
} from "../types";
import { logException } from "../utils/logger";

function structureToBack(structure: Structure) {
  const result = { ...structure, otherLabels: [] };
  if (structure.otherLabels) {
    result.otherLabels = structure.otherLabels
      .split(",")
      .filter((label) => label !== "")
      .map((label) => label.trim());
  }

  return result;
}

function structureToFront(structure: Structure): Structure {
  const result = { ...structure };
  if (Array.isArray(structure.otherLabels)) {
    result.otherLabels = structure.otherLabels.join(", ");
  }
  return result;
}

export async function siretWasAlreadyClaimed(siret: string) {
  const url = `${getApiURL()}/siret-claimed/${siret}`;
  const res = await fetch(url, {
    headers: {
      Accept: "application/json; version=1.0",
    },
  });

  const result = {
    ok: res.ok,
    status: res.status,
    result: undefined,
    error: undefined,
  };

  if (res.ok) {
    result.result = await res.json();
  } else {
    if (res.status !== 404) {
      try {
        result.error = await res.json();
      } catch (err) {
        console.error(err);
      }
    }
  }
  return result;
}

export async function getManagedStructures(
  searchText?: string
): Promise<ShortStructure[]> {
  const searchParam = searchText ? `&search=${searchText}` : "";
  const url = `${getApiURL()}/structures/?managed=1${searchParam}`;
  return (await fetchData<ShortStructure[]>(url)).data;
}

export async function getActiveStructures({
  pageSize,
  page,
}: {
  pageSize: number;
  page: number;
}) {
  const url = new URL("/structures/", getApiURL());

  url.searchParams.append("active", "1");
  url.searchParams.append("page_size", pageSize.toString());
  url.searchParams.append("page", page.toString());

  return (
    await fetchData<{ count: number; results: ShortStructure[] }>(
      url.toString()
    )
  ).data;
}

export async function getStructure(
  slug: string,
  fetch = window.fetch
): Promise<Structure | null> {
  const url = `${getApiURL()}/structures/${slug}/`;
  const structure = (await fetchData<Structure>(url, fetch)).data;
  return structure ? structureToFront(structure) : null;
}

export function createStructure(structure) {
  const url = `${getApiURL()}/structures/`;
  const method = "POST";
  return fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",

      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(structureToBack(structure)),
  });
}

export function modifyStructure(structure) {
  const url = `${getApiURL()}/structures/${structure.slug}/`;

  const method = "PATCH";
  return fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",

      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(structureToBack(structure)),
  });
}

let structuresOptions;

export async function getStructuresOptions(
  fetch = window.fetch
): Promise<StructuresOptions> {
  if (!structuresOptions) {
    const url = `${getApiURL()}/structures-options/`;
    const res = await fetchData<StructuresOptions>(url, fetch);
    structuresOptions = res.data;
  }
  return structuresOptions;
}

export async function getMembers(slug): Promise<Array<StructureMember> | null> {
  const url = `${getApiURL()}/structure-members/?structure=${slug}`;

  const result = await fetchData(url);
  if (result.ok) {
    return result.data as Array<StructureMember>;
  }
  return null;
}

export async function getPutativeMembers(
  slug
): Promise<Array<PutativeStructureMember> | null> {
  const url = `${getApiURL()}/structure-putative-members/?structure=${slug}`;

  const result = await fetchData(url);
  if (result.ok) {
    return result.data as Array<PutativeStructureMember>;
  }
  return null;
}

export async function deleteMember(uuid) {
  const url = `${getApiURL()}/structure-members/${uuid}/`;
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

export async function resendInvite(uuid) {
  const url = `${getApiURL()}/structure-putative-members/${uuid}/resend-invite/`;
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
  }
  return result;
}

export async function cancelInvite(uuid) {
  const url = `${getApiURL()}/structure-putative-members/${uuid}/cancel-invite/`;
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
  }
  return result;
}

export async function acceptMember(uuid) {
  const url = `${getApiURL()}/structure-putative-members/${uuid}/accept-membership-request/`;
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
  }
  return result;
}

export async function rejectMembershipRequest(uuid) {
  const url = `${getApiURL()}/structure-putative-members/${uuid}/reject-membership-request/`;
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
  }
  return result;
}
