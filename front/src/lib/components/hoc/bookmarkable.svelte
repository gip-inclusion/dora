<script lang="ts">
  import { clearBookmark, setBookmark } from "$lib/requests/services";
  import { refreshUserInfo, userInfo } from "$lib/utils/auth";

  export let slug: string;
  export let isDI = false;

  $: bookmarkId = $userInfo?.bookmarks?.find(
    (bookmark) => bookmark.slug === slug
  )?.id;

  async function handleFavClick() {
    if (bookmarkId) {
      await clearBookmark(bookmarkId);
    } else {
      await setBookmark(slug, isDI);
    }

    await refreshUserInfo();
  }
</script>

<slot onBookmark={handleFavClick} isBookmarked={!!bookmarkId} />
