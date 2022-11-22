<script context="module" lang="ts">
  import { getServicesOptions } from "$lib/services";
  import { getApiURL } from "$lib/utils/api.js";
  import { getQuery } from "./_homepage/_search";
  import { trackSearch } from "$lib/utils/plausible";
  import { SERVICE_UPDATE_STATUS, type SearchQuery } from "$lib/types";

  async function getResults({
    categoryIds,
    subCategoryIds,
    cityCode,
    cityLabel,
    kindIds,
    feeConditions,
  }: SearchQuery) {
    const query = getQuery({
      categoryIds,
      subCategoryIds,
      cityCode,
      cityLabel,
      kindIds,
      feeConditions,
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
    const categoryIds = query.get("cats") ? query.get("cats").split(",") : [];
    const subCategoryIds = query.get("subs")
      ? query.get("subs").split(",")
      : [];
    const cityCode = query.get("city");
    const cityLabel = query.get("cl");
    const kindIds = query.get("kinds") ? query.get("kinds").split(",") : [];
    const feeConditions = query.get("fees") ? query.get("fees").split(",") : [];

    let services = await getResults({
      categoryIds,
      subCategoryIds,
      cityCode,
      cityLabel,
      kindIds,
      feeConditions,
    });
    services.forEach((service) => {
      service.updateStatus = computeUpdateStatusData(service).updateStatus;
    });

    trackSearch(
      categoryIds,
      subCategoryIds,
      cityCode,
      cityLabel,
      kindIds,
      feeConditions,
      services.length
    );
    return {
      props: {
        categoryIds,
        subCategoryIds,
        cityCode,
        cityLabel,
        kindIds,
        feeConditions,
        allServices: services,
        servicesUpToDate: services.filter(
          (service) => service.updateStatus !== SERVICE_UPDATE_STATUS.REQUIRED
        ),
        servicesToUpdate: services.filter(
          (service) => service.updateStatus === SERVICE_UPDATE_STATUS.REQUIRED
        ),
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
    ServiceKind,
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
  import { computeUpdateStatusData } from "$lib/utils/service";
  import Notice from "$lib/components/notice.svelte";

  const PAGE_LENGTH = 10;

  export let servicesOptions: ServicesOptions;
  export let categoryIds: string[];
  export let subCategoryIds: string[];
  export let cityCode: string;
  export let cityLabel: string;
  export let kindIds: ServiceKind[];
  export let feeConditions: FeeCondition[];
  export let allServices: ServiceSearchResult[];
  export let servicesUpToDate: ServiceSearchResult[];
  export let servicesToUpdate: ServiceSearchResult[];

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
    cityCode && !isInDeploymentDepartments(cityCode, servicesOptions);
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
      {kindIds}
      {feeConditions}
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
    {#if allServices.length > 0}
      {allServices.length}
      {allServices.length > 1 ? "résultats" : "résultat"}
    {:else}
      Aucun résultat
    {/if}
  </div>

  {#if showDeploymentNotice}
    <div class="mt-s24">
      <DoraDeploymentNotice />
    </div>
  {/if}

  {#if hasOnlyNationalResults(allServices)}
    <div class="mt-s24">
      <OnlyNationalResultsNotice />
    </div>
  {/if}

  {#if allServices.length}
    <div class="mt-s32 flex flex-col gap-s16">
      <h2 class="sr-only">Résultats de votre recherche</h2>
      {#each servicesUpToDate as service, index}
        {#if index < currentPageLength}
          <SearchResult id={getResultId(index)} result={service} />
        {/if}
      {/each}

      {#if currentPageLength > servicesUpToDate.length && servicesToUpdate.length}
        <Notice
          type="warning"
          title="Les services qui suivent n’ont pas été mis à jour depuis plus de 8
        mois"
        />
        {#each servicesToUpdate as service, index}
          {#if index + servicesUpToDate.length < currentPageLength}
            <SearchResult
              id={getResultId(index + servicesUpToDate.length)}
              result={service}
            />
          {/if}
        {/each}
      {/if}

      {#if allServices.length > currentPageLength}
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

  {#if subCategoryIds.includes("famille--garde-enfants") || subCategoryIds.includes("famille--accompagnement-parents")}
    <SearchPromo />
  {/if}
</CenteredGrid>

<NewletterNotice />

<TallyNpsPopup formId={NPS_SEEKER_FORM_ID} />
