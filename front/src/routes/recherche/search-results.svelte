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
  import DoraDeploymentNotice from "./dora-deployment-notice.svelte";

  interface Props {
    data: PageData;
    filters: Filters;
    filteredServices: ServiceSearchResult[];
    selectedServiceSlug?: string;
    noAlertButtonBottomGap?: boolean;
    summarized?: boolean;
    noPagination?: boolean;
    showDeploymentNotice?: boolean;
    currentPageLength?: number;
  }

  const PAGE_LENGTH = 10;

  let {
    data,
    filters,
    filteredServices,
    selectedServiceSlug,
    noAlertButtonBottomGap = false,
    summarized = false,
    noPagination = false,
    showDeploymentNotice = false,
    currentPageLength = $bindable(PAGE_LENGTH),
  }: Props = $props();

  let creatingAlert = $state(false);

  let currentSearchWasAlreadySaved = $derived.by(() => {
    // Saved searches don't store the street address neither lat/lon
    const currentShortQueryString = getQueryString({
      categoryIds: [data.categoryIds[0] ? data.categoryIds[0] : ""],
      subCategoryIds: data.subCategoryIds.filter(
        (value) => !value.endsWith("--all")
      ),
      cityCode: data.cityCode,
      cityLabel: data.cityLabel,
      label: undefined,
      kindIds: filters.kinds.toSorted(),
      feeConditions: filters.feeConditions.toSorted(),
      locationKinds: filters.locationKinds.toSorted(),
      fundingLabels: filters.fundingLabels.toSorted(),
    });

    const userSavedSearches = $userInfo?.savedSearches || [];

    const result = userSavedSearches.some(
      (search) => getSavedSearchQueryString(search) === currentShortQueryString
    );
    return result;
  });

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
      fundingLabels: filters.fundingLabels.sort(),
    });
    await refreshUserInfo();
    creatingAlert = false;
  }
</script>

<div class="gap-s16 flex flex-col">
  <h2 class="sr-only">Résultats de votre recherche</h2>
  <div class="gap-s16 flex flex-col">
    {#each filteredServices as service, index}
      {#if noPagination || index < currentPageLength}
        <SearchResult
          id={getResultId(index)}
          result={service}
          searchId={data.searchId}
          selected={service.slug === selectedServiceSlug}
          {summarized}
        />
      {/if}
      {#if showDeploymentNotice && index === Math.min(4, filteredServices.length - 1)}
        <DoraDeploymentNotice />
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
        onclick={loadMoreResult}
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
        onclick={handleCreateAlertClick}
      />
    {/if}
  </div>
</div>
