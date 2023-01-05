<script lang="ts">
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import FavoriteIcon from "$lib/components/specialized/favorite-icon.svelte";
  import type { Bookmark } from "$lib/types";

  export let bookmark: Bookmark;

  $: service = bookmark.service;
</script>

<Bookmarkable slug={bookmark.service.slug} let:onBookmark let:isBookmarked>
  <div class="rounded-ml border border-gray-02 shadow-sm" tabindex="-1">
    <div class="p-s32 lg:pr-s64 ">
      <div class="mb-s24 flex items-center justify-between ">
        <a href="/structures/{service.structure}" class="block text-f14">
          {bookmark.service.structureInfo.name}
          {#if service.postalCode}<span
              class="legend ml-s8 font-bold text-gray-dark"
              >{service.postalCode} {service.city}</span
            >{/if}
        </a>
        <div class="flex items-center gap-s8">
          <FavoriteIcon on:click={onBookmark} active={isBookmarked} small />
        </div>
      </div>

      <h3 class=" mb-s0 text-france-blue lg:mb-s24">
        <a
          class="full-result-link hover:underline"
          href="/services/{service.slug}"
        >
          {service.name}
        </a>
      </h3>

      <p class="z-10 mt-s16 hidden text-f16 text-gray-text md:block">
        <a href="/services/{service.slug}">{service.shortDesc}</a>
      </p>
    </div>
  </div>
</Bookmarkable>

<style lang="postcss">
  /*
  * Link is on <h3> but we want all the card clickable (in an accessible way)
  * Source: http://inclusive-components.design/cards/
  */
  /* .full-result-link::after {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
  } */
</style>
