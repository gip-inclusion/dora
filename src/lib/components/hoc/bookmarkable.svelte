<script lang="ts">
  import { setBookmark } from "$lib/requests/services";
  import { refreshUserInfo, userInfo } from "$lib/utils/auth";

  export let slug: string;

  async function handleFavClick() {
    await setBookmark(slug, !isBookmarked);
    await refreshUserInfo();
  }

  $: isBookmarked = $userInfo?.bookmarks
    .map((b) => b.service.slug)
    .includes(slug);
</script>

<slot onBookmark={handleFavClick} {isBookmarked} />
