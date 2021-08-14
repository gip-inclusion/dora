import insane from "insane";

import { getApiURL, markdownToHTML } from "$lib/utils.js";
import { token } from "$lib/auth";
import { get } from "svelte/store";
import { writable } from "svelte/store";

export const structureOptions = writable(null);

export async function getStructures() {
  const url = `${getApiURL()}/structures/`;
  const res = await fetch(url, {
    headers: {
      Accept: "application/json; version=1.0",
    },
  });

  if (res.ok) {
    let structures = await res.json();
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
  const url = `${getApiURL()}/structures/${slug}`;
  const res = await fetch(url, {
    headers: {
      Accept: "application/json; version=1.0",
    },
  });

  if (res.ok) {
    let structure = await res.json();
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
    console.log(get(structureOptions));
  }

  return {
    status: res.status,
    error: new Error(`Could not load ${url}`),
  };
}
