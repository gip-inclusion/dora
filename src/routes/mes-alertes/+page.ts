import type { SavedSearch } from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import { fetchData } from "$lib/utils/misc";
import type { PageLoad } from "./$types";

export const ssr = false;

async function getSavedSearches() {
  const url = `${getApiURL()}/saved-searches/`;
  const result = await fetchData(url);
  if (result.ok) {
    return result.data as Array<SavedSearch>;
  }
  return [];
}

export const load: PageLoad = async ({ parent }) => {
  await parent();
  const savedSearches = getSavedSearches();
  return {
    title: "Mes alertes | DORA",
    noIndex: true,
    savedSearches,
  };
};
