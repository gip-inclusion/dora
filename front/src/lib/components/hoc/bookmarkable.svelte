<script lang="ts">
  import type { Snippet } from "svelte";

  import { clearBookmark, setBookmark } from "$lib/requests/services";
  import { refreshUserInfo, userInfo } from "$lib/utils/auth";

  interface Props {
    slug: string;
    isDI?: boolean;
    children?: Snippet<[any]>;
  }

  let { slug, isDI = false, children }: Props = $props();

  let bookmarkId = $derived(
    $userInfo?.bookmarks?.find((bookmark) => bookmark.slug === slug)?.id
  );

  async function handleFavClick() {
    if (bookmarkId) {
      await clearBookmark(bookmarkId);
    } else {
      await setBookmark(slug, isDI);
    }

    await refreshUserInfo();
  }
</script>

{@render children?.({ onBookmark: handleFavClick, isBookmarked: !!bookmarkId })}
