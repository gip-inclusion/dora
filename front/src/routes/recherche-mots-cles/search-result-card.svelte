<script lang="ts">
  import LoopLeftLineSystem from "svelte-remix/LoopLeftLineSystem.svelte";
  import MapPin2LineMap from "svelte-remix/MapPin2LineMap.svelte";
  import MoneyEuroCircleLineFinance from "svelte-remix/MoneyEuroCircleLineFinance.svelte";

  import LinkButton from "$lib/components/display/link-button.svelte";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import type { ServiceSearchResult } from "$lib/types";
  import { isNotFreeService } from "$lib/utils/service";

  interface Props {
    result: ServiceSearchResult;
    searchId: number | null;
    selected?: boolean;
    summarized?: boolean;
  }

  let {
    result,
    searchId,
    selected = false,
    summarized = false,
  }: Props = $props();

  let element: HTMLDivElement;

  let isDI = $derived(result.type === "di");

  let onSite = $derived(result.locationKinds.includes("en-presentiel"));
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
      class="rounded-2xl border shadow-sm"
      class:border-gray-02={!selected}
      class:border-magenta-cta={selected}
      tabindex="-1"
    >
      <div class="p-s32 lg:pr-s64 relative">
        <div class="text-f19 text-france-blue font-bold">
          {#if isDI}
            {result.structureInfo.name}
          {:else}
            <a
              class="hover:underline"
              href="/structures/{result.structureInfo.slug}"
            >
              {result.structureInfo.name}
            </a>
          {/if}
        </div>

        <!-- Service -->
        <h3 class="mb-s12 text-magenta-cta text-f19 my-s10">
          <a class="full-result-link hover:underline" href={servicePagePath}>
            {result.name}
          </a>
        </h3>

        {#if isDI}
          <div
            class="border-gray-02 px-s8 py-s2 text-f12 text-gray-text mb-s12 inline-block rounded-sm border"
          >
            Source&nbsp;: {result.diSourceDisplay}, via data·inclusion
          </div>
        {/if}

        {#if !summarized}
          <p class="mb-s12 text-f16 text-gray-text relative z-10">
            <a href={servicePagePath}>{result.shortDesc}</a>
          </p>
        {/if}

        <div
          class="mt-s16 gap-s16 flex flex-col items-start md:flex-row md:items-center md:justify-between"
        >
          <div class="gap-s8 text-f16 text-gray-dark flex flex-col">
            {#if result.modificationDate}
              <div
                class="text-service-green-darker gap-s6 text-f16 flex items-center font-bold"
              >
                <LoopLeftLineSystem size="20" />
                <RelativeDateLabel
                  date={result.modificationDate}
                  prefix="Actualisé"
                  bold
                />
              </div>
            {/if}
            {#if onSite}
              <div class="gap-s8 flex items-start">
                <span class="text-gray-text mt-s2 shrink-0">
                  <MapPin2LineMap size="20" />
                </span>
                <span>
                  Présentiel{#if result.address1}
                    &nbsp;- {result.address1}
                    {result.postalCode}&nbsp;{result.city}{/if}
                </span>
              </div>
            {/if}
            {#if remote}
              <div class="gap-s8 flex items-center">
                <span class="text-gray-text shrink-0">
                  <MapPin2LineMap size="20" />
                </span>
                <span>
                  {onSite ? "Également disponible à distance" : "À distance"}
                </span>
              </div>
            {/if}
            {#if result.feeCondition}
              <div class="gap-s8 flex items-center">
                <span class="text-gray-text shrink-0">
                  <MoneyEuroCircleLineFinance size="20" />
                </span>
                <span class:text-orange={isNotFreeService(result.feeCondition)}>
                  {isNotFreeService(result.feeCondition) ? "Payant" : "Gratuit"}
                </span>
              </div>
            {/if}
          </div>

          {#if !summarized}
            <LinkButton
              to={servicePagePath}
              label="Voir la fiche détaillée"
              secondary
              small
            />
          {/if}
        </div>
      </div>
    </div>
  {/snippet}
</Bookmarkable>
