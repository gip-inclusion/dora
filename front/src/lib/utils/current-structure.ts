import type { ShortStructure } from "$lib/types";
import type { UserInfo } from "./auth";
import type { UserPreferences } from "./preferences";

export function getCurrentlySelectedStructure(
  userInfo: UserInfo,
  preferences: UserPreferences
): ShortStructure | undefined {
  const userStructures = userInfo
    ? [...userInfo.structures, ...userInfo.pendingStructures]
    : [];

  return preferences.visitedStructures.length
    ? userStructures.find(
        ({ slug }) => slug === preferences.visitedStructures[0]
      )
    : userStructures[0];
}
