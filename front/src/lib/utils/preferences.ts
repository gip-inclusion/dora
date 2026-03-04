import { get, writable } from "svelte/store";
import type { ShortStructure } from "../types";

export interface UserPreferences {
  visitedStructures: string[];
}

export const userPreferences = writable<UserPreferences>({
  visitedStructures: [],
});

export function setCurrentStructure(slug: string): boolean {
  const current = get(userPreferences);
  if (current.visitedStructures[0] === slug) {
    return false;
  }

  const visitedStructures = current.visitedStructures.filter(
    (visitedStructureSlugs) => visitedStructureSlugs !== slug
  );
  visitedStructures.unshift(slug);

  localStorage.setItem("visitedStructures", JSON.stringify(visitedStructures));
  userPreferences.set({ visitedStructures });
  return true;
}

export function userPreferencesSet(userStructures: ShortStructure[]) {
  const userStructuresSlugs = userStructures.map((struct) => struct.slug);
  const visitedStructuresString = localStorage.getItem("visitedStructures");
  const visitedStructures = visitedStructuresString
    ? JSON.parse(visitedStructuresString).filter((slug) =>
        userStructuresSlugs.includes(slug)
      )
    : [];

  userPreferences.set({ visitedStructures });
}
