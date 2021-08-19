import { browser } from "$app/env";

import { writable, get } from "svelte/store";
import { storageKey } from "./_constants";

let stored;
if (browser) {
  const lsContent = localStorage.getItem(storageKey);
  if (lsContent) {
    stored = JSON.parse(lsContent);
  }
}
const defaultServiceCache = {
  kinds: [],
  categories: [],
  subcategories: [],
  beneficiariesAccessModes: [],
  coachOrientationModes: [],
  locationKind: [],
};

export const serviceCache = writable(
  stored || JSON.parse(JSON.stringify(defaultServiceCache))
);

export function resetServiceCache() {
  localStorage.removeItem(storageKey);
  serviceCache.set(defaultServiceCache);
}

export function persistServiceCache() {
  localStorage.setItem(storageKey, JSON.stringify(get(serviceCache)));
}

export const serviceOptions = writable(null);
