import { browser } from "$app/env";

import { writable } from "svelte/store";

let stored;
if (browser) {
  const lsContent = localStorage.getItem("currentSolution");
  if (lsContent) {
    stored = JSON.parse(lsContent);
  }
}

export const serviceCache = writable(
  stored || {
    kinds: [],
    categories: [],
    subcategories: [],
    beneficiariesAccessModes: [],
    coachOrientationModes: [],
    locationKind: [],
  }
);

export const serviceOptions = writable(null);
