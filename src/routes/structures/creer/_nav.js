import { goto } from "$app/navigation";
import { browser } from "$app/env";

import { getApiURL } from "$lib/utils";
import { token } from "$lib/auth";

import { get } from "svelte/store";
import { structureCache } from "./_creation-store.js";

import { storageKey } from "./_constants.js";

function persistStore() {
  if (browser) {
    localStorage.setItem(storageKey, JSON.stringify(get(structureCache)));
  }
}

function clearStore() {
  localStorage.removeItem(storageKey);
}

async function handleSubmit() {
  const url = `${getApiURL()}/structures/`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",

      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(get(structureCache)),
  });

  if (res.ok) {
    const structure = await res.json();
    clearStore();
    goto(`../${structure.id}`);
  }

  return {
    status: res.status,
    error: new Error(`Could not load ${url}`),
  };
}

export function persistAndGo(evt, backlink, forwardlink) {
  persistStore();
  if (evt.submitter.name === "backward") {
    goto(backlink);
  } else if (evt.submitter.name === "forward") {
    goto(forwardlink);
  } else if (evt.submitter.name === "validate") {
    handleSubmit();
  } else {
    console.log("Invalid submitter button name", evt.submitter.name);
  }
}
