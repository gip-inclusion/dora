import { get } from "svelte/store";

import { fetchData } from "$lib/utils.js";
import { getApiURL } from "$lib/utils/api.js";

import { token } from "$lib/auth";
import { logException } from "./logger";

import structureSchema from "$lib/schemas/structure.js";
import { validate } from "$lib/validation.js";

export async function siretWasAlreadyClaimed(siret) {
  const url = `${getApiURL()}/siret-claimed/${siret}`;
  const res = await fetch(url, {
    headers: {
      Accept: "application/json; version=1.0",
    },
  });

  const result = {
    ok: res.ok,
    status: res.status,
  };

  if (res.ok) {
    result.result = await res.json();
  } else {
    if (res.status !== 404)
      try {
        result.error = await res.json();
      } catch (err) {
        console.error(err);
      }
  }
  return result;
}

export async function getStructures() {
  const url = `${getApiURL()}/structures/`;
  return (await fetchData(url)).data;
}

export async function getStructure(slug) {
  const url = `${getApiURL()}/structures/${slug}/`;
  const result = (await fetchData(url)).data;

  return result;
}

export async function createStructure(structure) {
  const url = `${getApiURL()}/structures/`;
  const method = "POST";
  const res = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",

      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(structure),
  });

  const result = {
    ok: res.ok,
    status: res.status,
  };
  if (res.ok) {
    result.result = await res.json();
  } else {
    try {
      result.error = await res.json();
    } catch (err) {
      console.error(err);
    }
  }
  return result;
}

export async function modifyStructure(structure) {
  const url = `${getApiURL()}/structures/${structure.slug}/`;

  const method = "PATCH";
  const res = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",

      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(structure),
  });

  const result = {
    ok: res.ok,
    status: res.status,
  };
  if (res.ok) {
    result.result = await res.json();
  } else {
    try {
      result.error = await res.json();
    } catch (err) {
      console.error(err);
    }
  }
  return result;
}

let structuresOptions;
export async function getStructuresOptions() {
  if (!structuresOptions) {
    const url = `${getApiURL()}/structures-options/`;
    const res = await fetchData(url);
    structuresOptions = res.data;
  }
  return structuresOptions;
}

export async function getMembers(slug) {
  const url = `${getApiURL()}/structure-members/?structure=${slug}`;

  const result = await fetchData(url);
  if (result.ok) return result.data;
  return null;
}

export async function getPutativeMembers(slug) {
  const url = `${getApiURL()}/structure-putative-members/?structure=${slug}`;

  const result = await fetchData(url);
  if (result.ok) return result.data;
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

export function isStructureInformationsComplete(structure) {
  return validate(structure, structureSchema).valid;
}
