<script lang="ts">
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import FavoriteIcon from "$lib/components/specialized/favorite-icon.svelte";
  import type { Bookmark } from "$lib/types";

  export let bookmark: Bookmark;
</script>

<Bookmarkable
  slug={bookmark.slug}
  isDI={bookmark.isDi}
  let:onBookmark
  let:isBookmarked
>
  {@const service = bookmark.service}

  <div class="border-gray-02 rounded-2xl border shadow-sm" tabindex="-1">
    <div class="p-s32 lg:pr-s64">
      <div class="mb-s24 flex items-center justify-between">
        {#if !service?.name}
          <span class="text-f14 text-gray-text italic"
            >Impossible d’acceder à ce favori</span
          >
        {:else if bookmark.isDi}
          <div class="text-f14">
            {service?.structureName}
            {#if service?.postalCode}<span
                class="legend ml-s8 text-gray-dark font-bold"
                >{service?.postalCode} {service?.city}</span
              >{/if}
          </div>
        {:else}
          <a href="/structures/{service?.structureSlug}" class="text-f14 block">
            {service?.structureName}
            {#if service?.postalCode}<span
                class="legend ml-s8 text-gray-dark font-bold"
                >{service?.postalCode} {service.city}</span
              >{/if}
          </a>
        {/if}
        <div class="gap-s8 flex items-center">
          <FavoriteIcon on:click={onBookmark} active={isBookmarked} />
        </div>
      </div>

      {#if service?.name}
        <h3 class="mb-s0 text-france-blue lg:mb-s24">
          <a
            class="full-result-link hover:underline"
            href="/services/{bookmark.isDi ? 'di/' : ''}{bookmark?.slug}"
          >
            {service?.name}
          </a>
        </h3>

        <p class="mt-s16 text-f16 text-gray-text z-10 hidden md:block">
          <a href="/services/{bookmark.isDi ? 'di/' : ''}{bookmark?.slug}">
            {service?.shortDesc}
          </a>
        </p>
        {#if bookmark.isDi}
          <div
            class="border-gray-02 px-s8 py-s2 text-f12 text-gray-text inline rounded-sm border"
          >
            Source&nbsp;: <span class="capitalize">{service?.source}</span>, via
            data·inclusion
          </div>
        {/if}
      {/if}
    </div>
  </div>
</Bookmarkable>
