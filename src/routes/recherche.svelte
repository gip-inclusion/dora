<script context="module" lang="ts">
  import { getServicesOptions } from "$lib/services";
  import { getApiURL } from "$lib/utils/api.js";
  import { getQuery } from "./_homepage/_search";
  import { trackSearch } from "$lib/utils/plausible.js";

  async function getResults({
    categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    kindId,
    fee,
  }) {
    const query = getQuery({
      categoryIds,
      subCategoryIds,
      cityCode,
      cityLabel,
      kindId,
      fee,
    });
    const url = `${getApiURL()}/search/?${query}`;

    const res = await fetch(url, {
      headers: { Accept: "application/json; version=1.0" },
    });

    if (res.ok) {
      return await res.json();
    }

    // TODO: log errors
    try {
      console.error(await res.json());
    } catch (err) {
      console.error(err);
    }
    return [];
  }
  export async function load({ url }) {
    const query = url.searchParams;
    const categoryIds = query.get("cat") ? query.get("cat").split(",") : [];
    const subCategoryIds = query.get("sub") ? query.get("sub").split(",") : [];
    const cityCode = query.get("city");
    const cityLabel = query.get("cl");
    const kindId = query.get("kinds");
    const fee = query.get("fee") ? query.get("fee").split(",") : [];

    const services = await getResults({
      categoryIds,
      subCategoryIds,
      cityCode,
      cityLabel,
      kindId,
      fee,
    });
    trackSearch(
      categoryIds,
      subCategoryIds,
      cityCode,
      cityLabel,
      kindId,
      fee,
      services.length
    );
    return {
      props: {
        categoryIds,
        subCategoryIds,
        cityCode,
        cityLabel,
        kindId,
        fee,
        services,
        servicesOptions: await getServicesOptions(),
      },
    };
  }
</script>

<script lang="ts">
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import SearchResult from "./_homepage/_search-result.svelte";
  import SearchPromo from "./_homepage/_search-promo.svelte";

  import TallyNpsPopup from "$lib/components/tally-nps-popup.svelte";
  import { NPS_SEEKER_FORM_ID } from "$lib/const";
  import type {
    FeeCondition,
    ServiceSearchResult,
    ServicesOptions,
  } from "$lib/types";
  import Breadcrumb from "$lib/components/breadcrumb.svelte";
  import SearchForm from "./_homepage/_search-form.svelte";
  import ServiceSuggestionNotice from "./_homepage/_service-suggestion-notice.svelte";
  import DoraDeploymentNotice from "./_homepage/_dora-deployment-notice.svelte";
  import { isInDeploymentDepartments } from "$lib/utils/city";
  import OnlyNationalResultsNotice from "./_homepage/_only-national-results-notice.svelte";
  import NewletterNotice from "./_homepage/_newletter-notice.svelte";
  import { tick } from "svelte";
  import Button from "$lib/components/button.svelte";

  const PAGE_LENGTH = 10;

  export let servicesOptions: ServicesOptions;
  export let categoryIds: string[];
  export let subCategoryIds: string[];
  export let cityCode: string;
  export let cityLabel: string;
  export let kindId: string;
  export let fee: FeeCondition[];
  export let services;

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

  $: showDeploymentNotice = !isInDeploymentDepartments(
    cityCode,
    servicesOptions
  );
  $: {
    tags = [];

    if (categoryIds.length) {
      const categoryTags = categoryIds.map((id) => {
        return servicesOptions.categories.find((c) => c.value === id).label;
      });

      if (categoryTags.length) {
        tags = [...tags, ...categoryTags];
      }

      if (subCategoryIds.length) {
        const subCategoryTags = subCategoryIds.map((id) => {
          return servicesOptions.subcategories.find((c) => c.value === id)
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
    Services d’insertion {cityLabel ? `à ${cityLabel}` : ""} : {tags
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
      {servicesOptions}
      {cityCode}
      {cityLabel}
      {kindId}
      {fee}
      subCategoryIds={[
        ...subCategoryIds,
        ...categoryIds.map((c) => `${c}--all`),
      ]}
      showDeploymentWarning={false}
      useAdditionalFilters
    />
  </div>
</CenteredGrid>

<CenteredGrid extraClass="max-w-4xl m-auto">
  <div class="mt-s16 text-f21 font-bold text-gray-dark">
    {#if services.length > 0}
      {services.length}
      {services.length > 1 ? "résultats" : "résultat"}
    {:else}
      Aucun résultat
    {/if}
  </div>

  {#if showDeploymentNotice}
    <div class="mt-s24">
      <DoraDeploymentNotice />
    </div>
  {/if}

  {#if hasOnlyNationalResults(services)}
    <div class="mt-s24">
      <OnlyNationalResultsNotice />
    </div>
  {/if}

  {#if services.length}
    <div class="mt-s32 flex flex-col gap-s16">
      <h2 class="sr-only">Résultats de votre recherche</h2>
      {#each services as service, index}
        {#if index < currentPageLength}
          <SearchResult id={getResultId(index)} result={service} />
        {/if}
      {/each}

      {#if services.length > currentPageLength}
        <div class="text-center">
          <Button
            label="Charger plus de résultat"
            on:click={loadMoreResult}
            extraClass="!bg-transparent text-magenta-cta"
          />
        </div>
      {/if}
    </div>
  {/if}

  <div class="mt-s48 mb-s24 lg:flex lg:gap-s24">
    <ServiceSuggestionNotice />
  </div>

  {#if subCategoryIds.includes("famille--garde-enfants") || subCategoryIds.includes("famille--accompagnement-parents")}
    <SearchPromo />
  {/if}
</CenteredGrid>

<NewletterNotice />

<TallyNpsPopup formId={NPS_SEEKER_FORM_ID} />
