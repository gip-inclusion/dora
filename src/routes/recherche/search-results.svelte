<script lang="ts">
  import { tick } from "svelte";

  import type { ServiceSearchResult } from "$lib/types";
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import {
    getSavedSearchQueryString,
    saveSearch,
  } from "$lib/requests/saved-search";
  import { refreshUserInfo, userInfo } from "$lib/utils/auth";
  import { getQueryString } from "$lib/utils/service-search";

  import type { PageData } from "./$types";
  import CollectivityDirectoryBanner from "./collectivity-directory-banner.svelte";
  import type { Filters } from "./result-filters.svelte";
  import SearchResult from "./search-result.svelte";

  export let data: PageData;
  export let filters: Filters;
  export let filteredServices: ServiceSearchResult[];
  export let selectedServiceSlug: string | undefined = undefined;
  export let noAlertButtonBottomGap = false;
  export let summarized = false;
  export let noPagination = false;

  const PAGE_LENGTH = 10;

  let currentPageLength = PAGE_LENGTH;
  let creatingAlert = false;

  let currentSearchWasAlreadySaved;
  $: {
    // Saved searches don't store the street address neither lat/lon
    const currentShortQueryString = getQueryString({
      categoryIds: [data.categoryIds[0] ? data.categoryIds[0] : ""],
      subCategoryIds: data.subCategoryIds.filter(
        (value) => !value.endsWith("--all")
      ),
      cityCode: data.cityCode,
      cityLabel: data.cityLabel,
      label: undefined,
      kindIds: filters.kinds.sort(),
      feeConditions: filters.feeConditions.sort(),
      locationKinds: filters.locationKinds.sort(),
    });

    const userSavedSearches = $userInfo?.savedSearches || [];

    const result = userSavedSearches.some(
      (search) => getSavedSearchQueryString(search) === currentShortQueryString
    );
    currentSearchWasAlreadySaved = result;
  }

  function getResultId(index: number) {
    return `#result-${index}`;
  }

  async function loadMoreResult() {
    const oldPageLength = currentPageLength;
    currentPageLength += PAGE_LENGTH;
    await tick();

    // A11y : focus on the first new result
    const firstNewResult = document.getElementById(
      getResultId(oldPageLength)
    ) as HTMLElement;
    firstNewResult.focus();
  }

  async function handleCreateAlertClick() {
    creatingAlert = true;
    await saveSearch({
      category: data.categoryIds[0],
      subcategories: data.subCategoryIds.filter(
        (value) => !value.endsWith("--all")
      ),
      cityCode: data.cityCode,
      cityLabel: data.cityLabel,
      kinds: filters.kinds.sort(),
      fees: filters.feeConditions.sort(),
      locationKinds: filters.locationKinds.sort(),
    });
    await refreshUserInfo();
    creatingAlert = false;
  }
</script>

<div class="flex flex-col gap-s16">
  <h2 class="sr-only">Résultats de votre recherche</h2>
  <div class="flex flex-col gap-s16">
    {#each filteredServices as service, index}
      {#if noPagination || index < currentPageLength}
        <SearchResult
          id={getResultId(index)}
          result={service}
          searchId={data.searchId}
          categoryId={data.categoryIds[0]}
          subCategoryIds={[...data.subCategoryIds]}
          selected={service.slug === selectedServiceSlug}
          {summarized}
        />
      {/if}
      {#if index === 4}
        <CollectivityDirectoryBanner cityLabel={data.cityLabel} />
      {/if}
    {/each}
  </div>

  {#if !noPagination && filteredServices.length > currentPageLength}
    <div class="text-center">
      <Button
        label="Charger plus de résultats"
        on:click={loadMoreResult}
        noBackground
      />
    </div>
  {/if}

  <div
    class="sticky z-10 m-auto flex justify-center"
    class:bottom-s0={noAlertButtonBottomGap}
    class:bottom-s16={!noAlertButtonBottomGap}
  >
    {#if currentSearchWasAlreadySaved}
      <LinkButton to="/mes-alertes" secondary label="Voir mes alertes" />
    {:else}
      <Button
        label="Créer une alerte"
        disabled={!data.cityCode || creatingAlert}
        on:click={handleCreateAlertClick}
      />
    {/if}
  </div>
</div>
