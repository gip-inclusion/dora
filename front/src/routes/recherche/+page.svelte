<script lang="ts">
  import { onMount } from "svelte";

  import { page } from "$app/stores";

  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import SearchForm from "$lib/components/specialized/service-search.svelte";
  import { userInfo } from "$lib/utils/auth";
  import { isInDeploymentDepartments } from "$lib/utils/misc";

  import type { PageData } from "./$types";
  import DoraDeploymentNotice from "./dora-deployment-notice.svelte";
  import ServiceSuggestionNotice from "./service-suggestion-notice.svelte";
  import ResultFilters, { type Filters } from "./result-filters.svelte";
  import MapViewButton from "./map-view-button.svelte";
  import ResultCount from "./result-count.svelte";
  import SearchResults from "./search-results.svelte";
  import MesAidesDialog from "./mes-aides-dialog.svelte";
  import MonRecapPopup from "$lib/components/specialized/mon-recap-popup.svelte";

  export let data: PageData;

  const FILTER_KEY_TO_QUERY_PARAM = {
    kinds: "kinds",
    fundingLabels: "funding",
    feeConditions: "fees",
    locationKinds: "locs",
  };

  let filtersInitialized = false;

  let filters = Object.entries(FILTER_KEY_TO_QUERY_PARAM).reduce<Filters>(
    (acc, [filterKey, queryParam]) => ({
      ...acc,
      [filterKey]: $page.url.searchParams.get(queryParam)?.split(",") || [],
    }),
    {} as Filters
  );

  onMount(() => {
    // Vérifie si aucun filtre n'est sélectionné
    const noFilterSelected = Object.values(filters).every(
      (filter) => filter.length === 0
    );
    // Si aucun filtre n'est sélectionné, on présélectionne le filtre de lieu d'accueil « En présentiel »
    if (noFilterSelected) {
      filters.locationKinds.push("en-presentiel");
    }
  });

  function resetFilters() {
    filters = {
      kinds: [],
      fundingLabels: [],
      feeConditions: [],
      locationKinds: ["en-presentiel"],
    };
  }

  // Réinitialise les filtres quand la recherche est actualisée.
  // On observe l'objet data car celui-ci change à chaque fois que la recherche est actualisée.
  // Il n'est pas utile d'observer les champs de l'objet data vu que tout l'objet change.
  $: {
    data;
    if (filtersInitialized) {
      resetFilters();
    } else {
      filtersInitialized = true;
    }
  }

  // Filtre les services en fonctions des filtres sélectionnés
  $: filteredServices = data.services.filter((service) => {
    const kindsMatch =
      filters.kinds.length === 0 ||
      (service.kinds &&
        filters.kinds.some((value) => service.kinds!.includes(value)));
    const fundingLabelsMatch =
      filters.fundingLabels.length === 0 ||
      filters.fundingLabels.some((value) =>
        service.fundingLabels.includes(value)
      );
    const feeConditionMatch =
      filters.feeConditions.length === 0 ||
      (service.feeCondition &&
        filters.feeConditions.includes(service.feeCondition));
    const locationKindsMatch =
      filters.locationKinds.length === 0 ||
      filters.locationKinds.some((value) =>
        service.locationKinds.includes(value)
      );
    // Lorsqu'on ne veut que les services en présentiels, on exclue ceux à plus de 50 km de distance
    const onSiteAndNearby = !(
      filters.locationKinds.length === 1 &&
      filters.locationKinds[0] === "en-presentiel" &&
      service.distance > 50
    );
    return (
      kindsMatch &&
      fundingLabelsMatch &&
      feeConditionMatch &&
      locationKindsMatch &&
      onSiteAndNearby
    );
  });

  // Met à jour les paramètres d'URL en fonction des filtres sélectionnés
  $: {
    Object.keys(filters).forEach((filterKey) => {
      const queryParam = FILTER_KEY_TO_QUERY_PARAM[filterKey];
      if (filters[filterKey].length > 0) {
        $page.url.searchParams.set(queryParam, filters[filterKey]);
      } else {
        $page.url.searchParams.delete(queryParam);
      }
    });
    // Utilisation de l'API History pour mettre à jour les paramètres d'URL sans recharger la page
    window.history.replaceState(
      history.state,
      "",
      `?${$page.url.searchParams.toString()}`
    );
  }

  $: showDeploymentNotice =
    filteredServices.length < 10 &&
    !!data.cityCode &&
    !!data.servicesOptions &&
    !isInDeploymentDepartments(data.cityCode, data.servicesOptions);

  $: showMesAidesDialog = !$userInfo && data.categoryIds.includes("mobilite");
</script>

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
      label={data.label}
      lat={data.lat}
      lon={data.lon}
      kindIds={data.kindIds}
      feeConditions={data.feeConditions}
      locationKinds={data.locationKinds}
      fundingLabels={data.fundingLabels}
      categoryId={data.categoryIds[0]}
      subCategoryIds={[...data.subCategoryIds]}
      useAdditionalFilters
    />
  </div>
</CenteredGrid>

<CenteredGrid extraClass="m-auto">
  <div class="lg:gap-s24 lg:flex lg:flex-row lg:items-start">
    <div
      class="gap-s32 border-gray-02 p-s32 hidden flex-col rounded-2xl border shadow-sm lg:flex lg:basis-1/3"
    >
      <MapViewButton
        {data}
        availableFundingLabels={data.availableFundingLabels}
        bind:filters
        {filteredServices}
      />
      <ResultFilters
        servicesOptions={data.servicesOptions}
        availableFundingLabels={data.availableFundingLabels}
        bind:filters
      />
    </div>
    <div class="lg:basis-2/3">
      <div class="mt-s16 text-f21">
        <ResultCount
          resultCount={filteredServices.length}
          cityLabel={data.cityLabel}
        />
      </div>

      {#if filteredServices.length}
        <div class="mt-s32">
          <SearchResults
            {data}
            {filters}
            {filteredServices}
            {showDeploymentNotice}
          />
        </div>
      {:else if showDeploymentNotice}
        <div class="mt-s24">
          <DoraDeploymentNotice />
        </div>
      {/if}

      <div class="mb-s24 mt-s48 lg:gap-s24 lg:flex">
        <ServiceSuggestionNotice />
      </div>
    </div>
  </div>
</CenteredGrid>

{#if showMesAidesDialog}
  <MesAidesDialog />
{/if}

<MonRecapPopup />
