import {
  getMembers,
  getPutativeMembers,
  getStructure,
} from "$lib/requests/structures";
import { userInfo, type UserInfo } from "$lib/utils/auth";
import { trackStructure } from "$lib/utils/stats";
import {
  setCurrentStructure,
  userPreferences,
  type UserPreferences,
} from "$lib/utils/preferences";
import { error } from "@sveltejs/kit";
import type { LayoutLoad } from "./$types";
import { structure } from "./store";
import { browser } from "$app/environment";
import type { PutativeStructureMember, StructureMember } from "$lib/types";

export const load: LayoutLoad = async ({ fetch, params, parent, url }) => {
  await parent();

  const currentStructure = await getStructure(params.slug, fetch);

  if (!currentStructure) {
    error(404, "Page Not Found");
  }

  let preferences: UserPreferences;
  let info: UserInfo;

  userPreferences.subscribe((pref) => {
    preferences = pref;
  });

  userInfo.subscribe((newUserInfo: UserInfo) => {
    info = newUserInfo;
  });

  if (info && preferences) {
    const userStructuresSlugs = [
      ...info.pendingStructures,
      ...info.structures,
    ].map((struct) => struct.slug);

    if (userStructuresSlugs.includes(currentStructure.slug)) {
      setCurrentStructure(currentStructure.slug);
    }
  }

  // Récupération des membres
  let members: StructureMember[] = [];
  let putativeMembers: PutativeStructureMember[] = [];

  if (browser && info && currentStructure.canViewMembers) {
    const [membersResults, putativeMembersResults] = await Promise.all([
      getMembers(params.slug),
      getPutativeMembers(params.slug),
    ]);
    members = membersResults || [];
    putativeMembers = putativeMembersResults || [];
  }

  // TODO: can we get rid of this store, and just cascade the structure?
  structure.set(currentStructure);
  trackStructure(currentStructure, url, fetch);

  return {
    structure: currentStructure,
    members,
    putativeMembers,
  };
};
