<script lang="ts">
  import Breadcrumb from "$lib/components/breadcrumb.svelte";
  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import NewletterNotice from "$lib/components/newsletter/newletter-notice.svelte";
  import Notice from "$lib/components/notice.svelte";
  import SearchForm from "$lib/components/search/search-form.svelte";
  import TallyNpsPopup from "$lib/components/tally-nps-popup.svelte";
  import type { ServiceSearchResult } from "$lib/types";
  import { isInDeploymentDepartments } from "$lib/utils/city";
  import { TallyFormId } from "$lib/utils/nps";
  import { tick } from "svelte";
  import type { PageData } from "./$types";
  import DoraDeploymentNotice from "./dora-deployment-notice.svelte";
  import OnlyNationalResultsNotice from "./only-national-results-notice.svelte";
  import SearchPromo from "./search-promo.svelte";
  import SearchResult from "./search-result.svelte";
  import ServiceSuggestionNotice from "./service-suggestion-notice.svelte";

  export let data: PageData;

  const PAGE_LENGTH = 10;

  let tags = [];

  function hasOnlyNationalResults(services: ServiceSearchResult[]) {
    if (services.length === 0) return false;
    return services.every((s) => s.diffusionZoneType === "country");
  }

  let currentPageLength = PAGE_LENGTH;

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

  $: showDeploymentNotice =
    data.cityCode &&
    !isInDeploymentDepartments(data.cityCode, data.servicesOptions);
  $: {
    tags = [];

    if (data.categoryIds.length) {
      const categoryTags = data.categoryIds.map((id) => {
        return data.servicesOptions.categories.find((c) => c.value === id)
          .label;
      });

      if (categoryTags.length) {
        tags = [...tags, ...categoryTags];
      }

      if (data.subCategoryIds.length) {
        const subCategoryTags = data.subCategoryIds.map((id) => {
          return data.servicesOptions.subcategories.find((c) => c.value === id)
            .label;
        });

        if (subCategoryTags) {
          tags = [...tags, ...subCategoryTags];
        }
      }
    }
  }
</script>

<svelte:head>
  <title>
    Services d’insertion {data.cityLabel ? `à ${data.cityLabel}` : ""} : {tags
      .filter(Boolean)
      .join(", ")} | Recherche | DORA
  </title>
</svelte:head>

<CenteredGrid bgColor="bg-blue-light">
  <div>
    <h1 class="sr-only">
      Résultats de votre recherche de services d’insertion
    </h1>

    <div class="mb-s24">
      <Breadcrumb currentLocation="search" />
    </div>

    <SearchForm
      servicesOptions={data.servicesOptions}
      cityCode={data.cityCode}
      cityLabel={data.cityLabel}
      kindIds={data.kindIds}
      feeConditions={data.feeConditions}
      subCategoryIds={[
        ...data.subCategoryIds,
        ...data.categoryIds.map((c) => `${c}--all`),
      ]}
      showDeploymentWarning={false}
      useAdditionalFilters
    />
  </div>
</CenteredGrid>

<CenteredGrid extraClass="max-w-4xl m-auto">
  <div class="mt-s16 text-f21 font-bold text-gray-dark">
    {#if data.allServices.length > 0}
      {data.allServices.length}
      {data.allServices.length > 1 ? "résultats" : "résultat"}
    {:else}
      Aucun résultat
    {/if}
  </div>

  {#if showDeploymentNotice}
    <div class="mt-s24">
      <DoraDeploymentNotice />
    </div>
  {/if}

  {#if hasOnlyNationalResults(data.allServices)}
    <div class="mt-s24">
      <OnlyNationalResultsNotice />
    </div>
  {/if}

  {#if data.allServices.length}
    <div class="mt-s32 flex flex-col gap-s16">
      <h2 class="sr-only">Résultats de votre recherche</h2>
      {#each data.servicesUpToDate as service, index}
        {#if index < currentPageLength}
          <SearchResult id={getResultId(index)} result={service} />
        {/if}
      {/each}

      {#if currentPageLength > data.servicesUpToDate.length && data.servicesToUpdate.length}
        <Notice
          type="warning"
          title="Les services qui suivent n’ont pas été mis à jour depuis plus de 8
        mois"
        />
        {#each data.servicesToUpdate as service, index}
          {#if index + data.servicesUpToDate.length < currentPageLength}
            <SearchResult
              id={getResultId(index + data.servicesUpToDate.length)}
              result={service}
            />
          {/if}
        {/each}
      {/if}

      {#if data.allServices.length > currentPageLength}
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

  <div class="mt-s48 mb-s24 lg:flex lg:gap-s24">
    <ServiceSuggestionNotice />
  </div>

  {#if data.subCategoryIds.includes("famille--garde-enfants") || data.subCategoryIds.includes("famille--accompagnement-parents")}
    <SearchPromo />
  {/if}
</CenteredGrid>

<NewletterNotice />

<TallyNpsPopup formId={TallyFormId.NPS_SEEKER_FORM_ID} />
