<script lang="ts">
  import { userInfo, refreshUserInfo } from "$lib/auth";
  import { setBookmark } from "$lib/services";

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
