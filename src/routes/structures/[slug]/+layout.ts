import { getStructure } from "$lib/requests/structures";
import { userInfo, type UserInfo } from "$lib/utils/auth";
import { trackStructure } from "$lib/utils/plausible";
import { userPreferences, type UserPreferences } from "$lib/utils/preferences";
import { error } from "@sveltejs/kit";
import type { LayoutLoad } from "./$types";
import { structure } from "./store";

export const load: LayoutLoad = async ({ params, parent }) => {
  await parent();

  const s = await getStructure(params.slug);
  let preferences: UserPreferences;
  let info: UserInfo;

  userPreferences.subscribe((p) => {
    preferences = p;
  });

  userInfo.subscribe((u: UserInfo) => {
    info = u;
  });

  if (info && preferences) {
    const userStructuresSlugs = [
      ...info.pendingStructures,
      ...info.structures,
    ].map((us) => us.slug);

    if (userStructuresSlugs.includes(s.slug)) {
      const slugIndex = preferences.visitedStructures.indexOf(s.slug);

      if (slugIndex > 0) {
        preferences.visitedStructures.splice(slugIndex, 1);
      }

      preferences.visitedStructures.unshift(s.slug);

      localStorage.setItem(
        "visitedStructures",
        JSON.stringify(preferences.visitedStructures)
      );

      userPreferences.set(preferences);
    }
  }

  if (!s) {
    throw error(404, "Page Not Found");
  }

  // TODO: can we get rid of this store, and just cascade the structure?
  structure.set(s);
  trackStructure(s);

  return {
    structure: s,
  };
};
