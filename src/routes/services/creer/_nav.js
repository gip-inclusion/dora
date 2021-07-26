import { goto } from "$app/navigation";
import { browser } from "$app/env";

import { getApiURL } from "$lib/utils";
import { token } from "$lib/auth";

import { get } from "svelte/store";
import { service } from "./_creation-store.js";

import { storageKey } from "./_constants.js";

function persistStore() {
  if (browser) {
    localStorage.setItem(storageKey, JSON.stringify(get(service)));
  }
}

function clearStore() {
  localStorage.removeItem(storageKey);
}

async function handleSubmit() {
  const url = `${getApiURL()}/services/`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",

      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(get(service)),
  });

  if (res.ok) {
    const service = await res.json();
    clearStore();
    goto(`../${service.id}`);
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
