import insane from "insane";

import { get } from "svelte/store";

import { fetchData, htmlToMarkdown, markdownToHTML } from "$lib/utils.js";
import { getApiURL } from "$lib/utils/api.js";

import { token } from "$lib/auth";

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

export async function getMyStructures() {
  const url = `${getApiURL()}/structures/?mine=1`;
  return (await fetchData(url)).data;
}

export async function getStructure(slug) {
  const url = `${getApiURL()}/structures/${slug}/`;
  const result = (await fetchData(url)).data;
  if (result) {
    result.fullDesc = insane(markdownToHTML(result.fullDesc));
  }
  return result;
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

export async function getStructuresOptions() {
  const url = `${getApiURL()}/structures-options/`;
  return (await fetchData(url)).data;
}
