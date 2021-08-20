import insane from "insane";

import { getApiURL, htmlToMarkdown, markdownToHTML } from "$lib/utils.js";
import { token } from "$lib/auth";
import { get } from "svelte/store";
import { writable } from "svelte/store";

export const structureOptions = writable(null);

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
  const res = await fetch(url, {
    headers: {
      Accept: "application/json; version=1.0",
    },
  });

  if (res.ok) {
    const structures = await res.json();
    return {
      props: { structures },
    };
  }
  return {
    status: res.status,
    error: new Error(`Could not load ${url}`),
  };
}

export async function getStructure(slug) {
  const url = `${getApiURL()}/structures/${slug}/`;
  const res = await fetch(url, {
    headers: {
      Accept: "application/json; version=1.0",
    },
  });

  if (res.ok) {
    const structure = await res.json();
    structure.fullDesc = insane(markdownToHTML(structure.fullDesc));
    return {
      props: { structure },
    };
  }
  return {
    status: res.status,
    error: new Error(`Could not load ${url}`),
  };
}

export async function createStructure(structure) {
  if (structure.fullDesc)
    structure.fullDesc = htmlToMarkdown(structure.fullDesc);
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
  if (structure.fullDesc)
    structure.fullDesc = htmlToMarkdown(structure.fullDesc);
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

export async function fillStructuresOptions() {
  const url = `${getApiURL()}/structures/`;
  const res = await fetch(url, {
    method: "OPTIONS",
    headers: {
      Accept: "application/json; version=1.0",
      Authorization: `Token ${get(token)}`,
    },
  });

  if (res.ok) {
    structureOptions.set((await res.json()).actions.POST);
  }

  return {
    status: res.status,
    error: new Error(`Could not load ${url}`),
  };
}
