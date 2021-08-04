import { browser } from "$app/env";

import { writable } from "svelte/store";

import { storageKey } from "./_constants";
let stored;
if (browser) {
  const lsContent = localStorage.getItem(storageKey);
  if (lsContent) {
    stored = JSON.parse(lsContent);
  }
}

export const structureCache = writable(stored || {});

export const structureOptions = writable(null);
