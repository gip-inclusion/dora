import type { PageLoad } from "./$types";
import { getSavedSearches } from "#lib/requests/saved-search.js";

export const ssr = false;

export const load: PageLoad = async ({ parent, fetch }) => {
  await parent();

  return {
    savedSearches: getSavedSearches(fetch),
    title: "Mes alertes | DORA",
    noIndex: true,
  };
};
