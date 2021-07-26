import { browser } from "$app/env";

import { writable } from "svelte/store";

let stored;
if (browser) {
  const lsContent = localStorage.getItem("currentSolution");
  if (lsContent) {
    stored = JSON.parse(lsContent);
  }
}

export const service = writable(
  stored || {
    kinds: [],
    categories: [],
    beneficiariesAccessModes: [],
    coachOrientationModes: [],
    locationKind: [],
  }
);
