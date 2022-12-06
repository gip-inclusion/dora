import { writable } from "svelte/store";
import type { ShortStructure } from "./types";

export interface UserPreferences {
  visitedStructures: ShortStructure[];
}

export const userPreferences = writable<UserPreferences>({
  visitedStructures: [],
});

export function userPreferencesSet(userStructures: ShortStructure[]) {
  const userStructuresSlugs = userStructures.map((s) => s.slug);
  const visitedStructuresString = localStorage.getItem("visitedStructures");
  const visitedStructures = visitedStructuresString
    ? JSON.parse(visitedStructuresString).filter((slug) =>
        userStructuresSlugs.includes(slug)
      )
    : [];

  userPreferences.set({ visitedStructures });
}
