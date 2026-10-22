import { get } from "svelte/store";
import type { PageLoad } from "./$types";
import { userInfo } from "#lib/utils/auth.js";
import { getBookmarks } from "#lib/requests/services.js";
import type { Bookmark } from "#lib/types.js";

export const load: PageLoad = async ({ fetch, parent }) => {
  await parent();

  const user = get(userInfo);
  if (!user) {
    return {};
  }

  const bookmarks: Bookmark[] = await getBookmarks(fetch);

  return {
    title: "Mes favoris | DORA",
    noIndex: true,
    bookmarks,
  };
};
