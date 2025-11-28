import type { ShortStructure } from "$lib/types";
import type { UserInfo } from "./auth";
import type { UserPreferences } from "./preferences";

export function getCurrentlySelectedStructure(
  userInfo: UserInfo | null,
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

export function isMemberOrPotentialMemberOfStructure(
  userInfo: UserInfo | null,
  structureSlug: string
): boolean {
  if (!userInfo) {
    return false;
  }
  return (
    userInfo.structures.some(({ slug }) => slug === structureSlug) ||
    userInfo.pendingStructures.some(({ slug }) => slug === structureSlug)
  );
}
