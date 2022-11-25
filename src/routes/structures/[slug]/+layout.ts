import { userInfo } from "$lib/auth";
import { userPreferences } from "$lib/preferences";
import { getStructure } from "$lib/structures";
import { trackStructure } from "$lib/utils/plausible";
import { error } from "@sveltejs/kit";
import { structure } from "./_store";

export async function load({ params, parent }) {
  await parent();

  const s = await getStructure(params.slug);
  let preferences;
  let info;

  userPreferences.subscribe((p) => {
    preferences = p;
  });

  userInfo.subscribe((u) => {
    info = u;
  });

  if (preferences) {
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

  structure.set(s);
  trackStructure(s);

  return {};
}
