import { getRecentSearchResults } from "$lib/requests/saved-search";
import { token, userInfo } from "$lib/utils/auth";
import { error, redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async ({ fetch, url, params, parent }) => {
  await parent();
  if (!get(token)) {
    redirect(
      302,
      `/auth/connexion?next=${encodeURIComponent(url.pathname + url.search)}`
    );
  }

  const savedSearch = get(userInfo)?.savedSearches.find(
    (search) => search.id === Number(params.searchId)
  );
  if (!savedSearch) {
    error(404);
  }

  const recentResults = await getRecentSearchResults(savedSearch.id, fetch);

  return {
    title: `Mon alerte | DORA`,
    savedSearch,
    recentResults,
  };
};
