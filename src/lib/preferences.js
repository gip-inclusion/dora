import { writable } from "svelte/store";

export const userPreferences = writable(null);

export function userPreferencesSet() {
  const visitedStructuresString = localStorage.getItem("structuresViewed");
  const visitedStructures = visitedStructuresString
    ? JSON.parse(visitedStructuresString)
    : [];

  userPreferences.set({ visitedStructures });
}
