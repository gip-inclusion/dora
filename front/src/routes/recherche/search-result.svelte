<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import FavoriteIcon from "$lib/components/specialized/favorite-icon.svelte";
  import type { ServiceSearchResult } from "$lib/types";

  interface Props {
    id: string;
    result: ServiceSearchResult;
    searchId: number | null;
    selected?: boolean;
    summarized?: boolean;
  }

  let {
    id,
    result,
    searchId,
    selected = false,
    summarized = false,
  }: Props = $props();

  let element: HTMLDivElement;

  let isDI = $derived(result.type === "di");

  let onSite = $derived(
    result.locationKinds.includes("en-presentiel") &&
      result.distance != null &&
      result.distance <= 50
  );
  let remote = $derived(result.locationKinds.includes("a-distance"));

  let servicePagePath = $derived(
    `/services/${isDI ? "di--" : ""}${result.slug}?searchId=${searchId}`
  );

  $effect(() => {
    if (selected) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "center",
        inline: "center",
      });
    }
  });
</script>

<Bookmarkable slug={result.slug} {isDI}>
  {#snippet children({ onBookmark, isBookmarked })}
    <div
      bind:this={element}
      {id}
      class="rounded-2xl border shadow-sm"
      class:border-gray-02={!selected}
      class:border-magenta-cta={selected}
      tabindex="-1"
    >
      <div class="p-s32 lg:pr-s64 relative">
        <div class="mb-s4 flex items-center justify-between">
          <div class="text-f14">
            {result.structureInfo.name}
          </div>
          <div class="gap-s8 flex items-center">
            <FavoriteIcon on:click={onBookmark} active={isBookmarked} />
          </div>
        </div>

        <h3 class="mb-s12 text-france-blue">
          <a class="full-result-link hover:underline" href={servicePagePath}>
            {result.name}
          </a>
        </h3>

        <div class="gap-s6 flex flex-wrap items-baseline">
          {#if onSite}
            <div class="text-f16 text-france-blue">
              {#if result.address1}
                {result.address1}{#if result.address2}, {result.address2}{/if},
              {/if}
              {result.postalCode}&nbsp;{result.city}
            </div>
            <!-- On n'affiche pas la distance lorsqu'elle n'est pas fournie ou
                 lorsqu'il s'agit d'un service DORA et que la distance est de 0. -->
            {#if typeof result.distance === "number" && !(!isDI && result.distance === 0)}
              <div class="tag">
                {#if result.distance === 0}
                  &lt; 1 km
                {:else}
                  à&nbsp;{result.distance < 10
                    ? Math.round(result.distance * 10) / 10
                    : Math.round(result.distance)} km
                {/if}
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

        {#if !summarized}
          <p
            class="mt-s16 text-f16 text-gray-text relative z-10 hidden md:block"
          >
            <a href={servicePagePath}>{result.shortDesc}</a>
          </p>
          <div
            class={`mt-s24 gap-s24 flex flex-col items-center md:flex-row ${isDI ? "justify-between" : "justify-end"}`}
          >
            {#if isDI}
              <div
                class="border-gray-02 px-s8 py-s2 text-f12 text-gray-text inline rounded-sm border"
              >
                Source&nbsp;: {result.diSourceDisplay}, via data·inclusion
              </div>
            {/if}
            <LinkButton
              to={servicePagePath}
              label="Voir la fiche détaillée"
              secondary
              small
            />
          </div>
        {/if}
      </div>
    </div>
  {/snippet}
</Bookmarkable>

<style lang="postcss">
  @reference "../../app.css";

  .tag {
    @apply bg-blue-information px-s8 py-s0 text-f14 text-france-blue rounded-3xl whitespace-nowrap;
  }
</style>
