<script lang="ts">
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import FavoriteIcon from "$lib/components/specialized/favorite-icon.svelte";
  import type { ServiceSearchResult } from "$lib/types";

  export let id: string;
  export let result: ServiceSearchResult;
  export let searchId: string;
  $: hasLocationTag = result.distance || result.location === "À distance";
  $: isDI = result.type === "di";
</script>

<Bookmarkable slug={result.slug} {isDI} let:onBookmark let:isBookmarked>
  <div {id} class="rounded-ml border border-gray-02 shadow-sm" tabindex="-1">
    <div class="relative p-s32 lg:pr-s64">
      <div class="mb-s24 flex items-center justify-between">
        <div class="text-f14">
          {result.structureInfo.name}
          {#if result.location && result.location !== "À distance"}<span
              class="legend ml-s8 font-bold text-gray-dark"
              >{result.location}</span
            >{/if}
        </div>
        <div class="flex items-center gap-s8">
          {#if hasLocationTag}
            <div
              class="whitespace-nowrap rounded-xl bg-france-blue px-s10 py-s4 text-f14 font-bold text-white"
            >
              {#if result.distance}
                à&nbsp;{Math.round(result.distance)}&nbsp;km
              {/if}
              {#if result.location === "À distance"}
                À distance
              {/if}
            </div>
          {/if}
          <FavoriteIcon on:click={onBookmark} active={isBookmarked} small />
        </div>
      </div>

      <h3 class="mb-s0 text-france-blue lg:mb-s24">
        <a
          class="full-result-link hover:underline"
          href="/services/{isDI
            ? `di/`
            : ``}{result.slug}?searchId={searchId.event}"
        >
          {result.name}
        </a>
      </h3>

      <p class="relative z-10 mt-s16 hidden text-f16 text-gray-text md:block">
        <a
          href="/services/{isDI
            ? `di/`
            : ``}{result.slug}?searchId={searchId.event}">{result.shortDesc}</a
        >
      </p>
      {#if isDI}
        <div
          class="inline rounded border border-gray-02 px-s8 py-s2 text-f12 text-gray-text"
        >
          Source&nbsp;: {result.diSourceDisplay}, via data·inclusion
        </div>
      {/if}
    </div>
  </div>
</Bookmarkable>
