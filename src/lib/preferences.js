import { writable } from "svelte/store";

export const userPreferences = writable(null);

export function userPreferencesSet(userStructures) {
  const userStructuresSlugs = userStructures.map((s) => s.slug);
  const visitedStructuresString = localStorage.getItem("visitedStructures");
  const visitedStructures = visitedStructuresString
    ? JSON.parse(visitedStructuresString).filter((slug) =>
        userStructuresSlugs.includes(slug)
      )
    : [];

  userPreferences.set({ visitedStructures });
}
