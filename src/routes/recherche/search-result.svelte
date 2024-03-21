<script lang="ts">
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import FavoriteIcon from "$lib/components/specialized/favorite-icon.svelte";
  import type { ServiceSearchResult } from "$lib/types";

  export let id: string;
  export let result: ServiceSearchResult;
  export let searchId: string | null;

  $: isDI = result.type === "di";

  $: onSite =
    result.locationKinds.includes("en-presentiel") &&
    result.distance != null &&
    result.distance <= 50;
  $: remote = result.locationKinds.includes("a-distance");
</script>

<Bookmarkable slug={result.slug} {isDI} let:onBookmark let:isBookmarked>
  <div {id} class="rounded-ml border border-gray-02 shadow-sm" tabindex="-1">
    <div class="relative p-s32 lg:pr-s64">
      <div class="mb-s4 flex items-center justify-between">
        <div class="text-f14">
          {result.structureInfo.name}
        </div>
        <div class="flex items-center gap-s8">
          <FavoriteIcon on:click={onBookmark} active={isBookmarked} />
        </div>
      </div>

      <h3 class="mb-s12 text-france-blue">
        <a
          class="full-result-link hover:underline"
          href="/services/{isDI
            ? `di--`
            : ``}{result.slug}?searchId={searchId?.event}"
        >
          {result.name}
        </a>
      </h3>

      <div class="flex flex-wrap items-baseline gap-s6">
        {#if onSite}
          <div class="text-f16 text-france-blue">
            {result.address1}{#if result.address2}, {result.address2}{/if},
            {result.postalCode}&nbsp;{result.city}
          </div>
          {#if result.distance > 0}
            <div class="tag">
              à&nbsp;{result.distance < 10
                ? Math.round(result.distance * 10) / 10
                : Math.round(result.distance)}&nbsp;km
            </div>
          {/if}
        {/if}
        {#if remote}
          <div class="tag">
            {#if onSite}
              Également disponible à distance
            {:else}
              À distance
            {/if}
          </div>
        {/if}
      </div>

      <p class="relative z-10 mt-s16 hidden text-f16 text-gray-text md:block">
        <a
          href="/services/{isDI
            ? `di--`
            : ``}{result.slug}?searchId={searchId?.event}">{result.shortDesc}</a
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

<style lang="postcss">
  .tag {
    @apply whitespace-nowrap rounded-xl bg-blue-information px-s8 py-s0 text-f14  text-france-blue;
  }
</style>
