<script module lang="ts">
  export const SEARCH_RESULTS_PAGE_LENGTH = 10;
</script>

<script lang="ts">
  import { tick } from "svelte";

  import type { ServiceSearchResult } from "$lib/types";
  import Button from "$lib/components/display/button.svelte";

  import type { PageData } from "./$types";
  import SearchResultCard from "./search-result-card.svelte";

  interface Props {
    data: PageData;
    filteredServices: ServiceSearchResult[];
    selectedServiceSlug?: string;
    summarized?: boolean;
    noPagination?: boolean;
    currentPageLength?: number;
  }

  let {
    data,
    filteredServices,
    selectedServiceSlug,
    summarized = false,
    noPagination = false,
    currentPageLength = $bindable(SEARCH_RESULTS_PAGE_LENGTH),
  }: Props = $props();

  function getResultId(index: number) {
    return `#result-${index}`;
  }

  async function loadMoreResult() {
    const oldPageLength = currentPageLength;
    currentPageLength += SEARCH_RESULTS_PAGE_LENGTH;
    await tick();

    // A11y : focus on the first new result
    const firstNewResult = document.getElementById(
      getResultId(oldPageLength)
    ) as HTMLElement;
    firstNewResult.focus();
  }
</script>

<div class="gap-s16 flex flex-col">
  <h2 class="sr-only">Résultats de votre recherche</h2>
  <div class="gap-s16 flex flex-col">
    {#each filteredServices as service, index}
      {#if noPagination || index < currentPageLength}
        <SearchResultCard
          id={getResultId(index)}
          result={service}
          searchId={data.searchId}
          selected={service.slug === selectedServiceSlug}
          {summarized}
        />
      {/if}
    {/each}
  </div>

  {#if !noPagination && filteredServices.length > currentPageLength}
    <div class="text-center">
      <Button
        label="Charger plus de résultats"
        onclick={loadMoreResult}
        noBackground
      />
    </div>
  {/if}
</div>
