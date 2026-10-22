import { fetchData } from "#lib/utils/misc.js";
import { getApiURL } from "#lib/utils/api.js";
import { getCurrentlySelectedStructure } from "#lib/utils/current-structure.js";
import { get } from "svelte/store";

import { userInfo } from "#lib/utils/auth.js";
import { userPreferences } from "#lib/utils/preferences.js";
import type { OrientationStats } from "#lib/types.js";

export const ssr = false;

export const load = async ({ parent, fetch }) => {
  await parent();

  const structure = getCurrentlySelectedStructure(
    get(userInfo),
    get(userPreferences)
  );

  const url = `${getApiURL()}/structures/${structure?.slug}/orientations/stats/`;
  const result = await fetchData<OrientationStats>(url, fetch);

  return {
    title: "Suivi des orientations",
    noIndex: true,
    stats: result.data
      ? result.data
      : {
          totalSent: 0,
          totalSentPending: 0,
          totalReceived: 0,
          totalReceivedPending: 0,
          structureHasServices: false,
        },
    structure: structure
      ? structure
      : { name: "Pas trouvé", slug: "Pas trouvé" },
  };
};
