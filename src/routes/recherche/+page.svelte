<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import SearchForm from "$lib/components/specialized/service-search.svelte";
  import {
    getSavedSearchQueryString,
    saveSearch,
  } from "$lib/requests/saved-search";
  import type { ServiceSearchResult } from "$lib/types";
  import { refreshUserInfo, userInfo } from "$lib/utils/auth";
  import { isInDeploymentDepartments } from "$lib/utils/misc";
  import { getQueryString } from "$lib/utils/service-search";

  import { tick } from "svelte";
  import type { PageData } from "./$types";
  import DoraDeploymentNotice from "./dora-deployment-notice.svelte";
  import OnlyNationalResultsNotice from "./only-national-results-notice.svelte";
  import SearchPromo from "./search-promo.svelte";
  import SearchResult from "./search-result.svelte";
  import ServiceSuggestionNotice from "./service-suggestion-notice.svelte";

  export let data: PageData;

  const PAGE_LENGTH = 10;

  let currentPageLength = PAGE_LENGTH;

  let creatingAlert = false;

  function hasOnlyNationalResults(services: ServiceSearchResult[]) {
    if (services.length === 0) {
      return false;
    }
    return services.every((service) => service.diffusionZoneType === "country");
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
      kinds: data.kindIds,
      fees: data.feeConditions,
      locationKinds: data.locationKinds,
    });
    await refreshUserInfo();
    creatingAlert = false;
  }

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
      kindIds: data.kindIds,
      feeConditions: data.feeConditions,
      locationKinds: data.locationKinds,
    });

    const userSavedSearches = $userInfo?.savedSearches || [];

    const result = userSavedSearches.some(
      (search) => getSavedSearchQueryString(search) === currentShortQueryString
    );
    currentSearchWasAlreadySaved = result;
  }

  $: showDeploymentNotice =
    data.cityCode &&
    !isInDeploymentDepartments(data.cityCode, data.servicesOptions);
</script>

<CenteredGrid bgColor="bg-blue-light">
  <div>
    <h1 class="sr-only">
      Résultats de votre recherche de services d’insertion
    </h1>

    <div class="mb-s24">
      <Breadcrumb currentLocation="search" dark />
    </div>

    <SearchForm
      servicesOptions={data.servicesOptions}
      cityCode={data.cityCode}
      cityLabel={data.cityLabel}
      label={data.label}
      lat={data.lat}
      lon={data.lon}
      kindIds={data.kindIds}
      feeConditions={data.feeConditions}
      locationKinds={data.locationKinds}
      categoryId={data.categoryIds[0]}
      subCategoryIds={[...data.subCategoryIds]}
      showDeploymentWarning={false}
      useAdditionalFilters
    />
  </div>
</CenteredGrid>

<CenteredGrid extraClass="max-w-4xl m-auto">
  <div class="mt-s16 text-f21">
    {data.services.length > 0 ? data.services.length : "Aucun"}
    {data.services.length > 1 ? "services" : "service"}
    à proximité de <b>{data.cityLabel}</b>
  </div>

  {#if showDeploymentNotice}
    <div class="mt-s24">
      <DoraDeploymentNotice />
    </div>
  {/if}

  {#if hasOnlyNationalResults(data.services)}
    <div class="mt-s24">
      <OnlyNationalResultsNotice />
    </div>
  {/if}

  {#if data.services.length}
    <div class="mt-s32 flex flex-col gap-s16">
      <h2 class="sr-only">Résultats de votre recherche</h2>
      {#each data.services as service, index}
        {#if index < currentPageLength}
          <SearchResult
            id={getResultId(index)}
            result={service}
            searchId={data.searchId}
          />
        {/if}
      {/each}

      <div class="sticky bottom-s16 z-10 m-auto flex justify-center">
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

      {#if data.services.length > currentPageLength}
        <div class="text-center">
          <Button
            label="Charger plus de résultats"
            on:click={loadMoreResult}
            noBackground
          />
        </div>
      {/if}
    </div>
  {/if}

  <div class="mb-s24 mt-s48 lg:flex lg:gap-s24">
    <ServiceSuggestionNotice />
  </div>

  {#if data.subCategoryIds.includes("famille--garde-enfants") || data.subCategoryIds.includes("famille--accompagnement-parents")}
    <SearchPromo />
  {/if}
</CenteredGrid>
