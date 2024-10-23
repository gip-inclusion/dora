import { get } from "svelte/store";
import type { PageLoad } from "./$types";
import { userInfo } from "$lib/utils/auth";
import { getBookmarks } from "$lib/requests/services";
import type { Bookmark } from "$lib/types";

export const load: PageLoad = async ({ parent }) => {
  await parent();

  const user = get(userInfo);
  if (!user) {
    return {};
  }

  const bookmarks: Bookmark[] = await getBookmarks();

  return {
    title: "Mes favoris | DORA",
    noIndex: true,
    bookmarks,
  };
};
