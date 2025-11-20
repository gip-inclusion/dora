import { fetchData } from "$lib/utils/misc";
import { getApiURL } from "$lib/utils/api";
import { getCurrentlySelectedStructure } from "$lib/utils/current-structure";
import { get } from "svelte/store";

import { userInfo } from "$lib/utils/auth";
import { userPreferences } from "$lib/utils/preferences";
import type { OrientationStats } from "$lib/types";

export const ssr = false;

export const load = async ({ parent, fetch }) => {
  await parent();

  const structure = getCurrentlySelectedStructure(
    get(userInfo),
    get(userPreferences)
  );

  const url = `${getApiURL()}/orientations/stats/${structure?.slug}/`;
  const result = await fetchData<OrientationStats>(url, fetch);

  return {
    title: "Suivi des orientations",
    noIndex: true,
    stats: result?.data,
    structure,
  };
};
