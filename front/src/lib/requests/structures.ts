import { getApiURL } from "$lib/utils/api";
import { fetchData } from "$lib/utils/misc";
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
  const result = await fetchData<Structure>(url);
  if (result.ok) {
    return result.data;
  } else if (result.status === 404) {
    return null;
  } else {
    throw Error(result.statusText);
  }
}

export async function getManagedStructures(
  searchText?: string
): Promise<ShortStructure[]> {
  const searchParam = searchText ? `&search=${searchText}` : "";
  const url = `${getApiURL()}/structures/?managed=1${searchParam}`;
  try {
    const result = await fetchData<ShortStructure[]>(url);
    if (!result.ok) {
      logException(
        new Error(`getManagedStructures: ${result.status} ${result.error}`)
      );
    }
    return result.data ?? [];
  } catch (err) {
    logException(err);
    return [];
  }
}

export async function getActiveStructures({
  pageSize,
  page,
}: {
  pageSize: number;
  page: number;
}) {
  const params = new URLSearchParams();
  params.append("active", "1");
  params.append("page_size", pageSize.toString());
  params.append("page", page.toString());
  const url = `${getApiURL()}/structures/?${params}`;

  return (await fetchData<{ count: number; results: ShortStructure[] }>(url))
    .data;
}

export async function getStructure(
  slug: string,
  fetchFunction = fetch
): Promise<Structure | null> {
  const url = `${getApiURL()}/structures/${slug}/`;
  const structure = (await fetchData<Structure>(url, fetchFunction)).data;
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
    },
    body: JSON.stringify(structureToBack(structure)),
  });
}

let structuresOptions;

export async function getStructuresOptions(
  fetchFunction = fetch
): Promise<StructuresOptions> {
  if (!structuresOptions) {
    const url = `${getApiURL()}/structures-options/`;
    const res = await fetchData<StructuresOptions>(url, fetchFunction);
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
