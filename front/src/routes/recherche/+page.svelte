<script lang="ts">
  import { onMount, tick, untrack } from "svelte";
  import { browser } from "$app/environment";

  import { page } from "$app/stores";

  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import MonRecapPopup from "$lib/components/specialized/mon-recap-popup.svelte";
  import SearchForm from "$lib/components/specialized/service-search.svelte";
  import { userInfo } from "$lib/utils/auth";
  import { isInDeploymentDepartments } from "$lib/utils/misc";

  import type { PageData } from "./$types";
  import DoraDeploymentNotice from "./dora-deployment-notice.svelte";
  import MapViewButton from "./map-view-button.svelte";
  import MesAidesDialog from "./mes-aides-dialog.svelte";
  import ResultCount from "./result-count.svelte";
  import ResultFilters, { type Filters } from "./result-filters.svelte";
  import SearchResults from "./search-results.svelte";
  import { SEARCH_RESULTS_PAGE_LENGTH } from "./search-results.svelte";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  interface SnapshotState {
    scrollY: number;
    filters: Filters;
    currentPageLength: number;
  }

  const FILTER_KEY_TO_QUERY_PARAM = {
    kinds: "kinds",
    fundingLabels: "funding",
    feeConditions: "fees",
    locationKinds: "locs",
  };

  let filtersInitialized = $state(false);

  let filters = $state(
    Object.entries(FILTER_KEY_TO_QUERY_PARAM).reduce<Filters>(
      (acc, [filterKey, queryParam]) => ({
        ...acc,
        [filterKey]: $page.url.searchParams.get(queryParam)?.split(",") || [],
      }),
      {} as Filters
    )
  );

  let currentPageLength = $state(SEARCH_RESULTS_PAGE_LENGTH);

  export const snapshot = {
    capture: (): SnapshotState | null => {
      if (!browser) {
        return null;
      }

      return {
        scrollY: window.scrollY,
        filters: JSON.parse(JSON.stringify(filters)),
        currentPageLength,
      };
    },
    restore: async (state: SnapshotState | null) => {
      if (!browser || !state) {
        return;
      }

      filters = state.filters;
      currentPageLength = state.currentPageLength;
      await tick();
      window.scrollTo(0, state.scrollY);
    },
  };

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
    // Réinitialise aussi la pagination quand on change les filtres
    currentPageLength = SEARCH_RESULTS_PAGE_LENGTH;
  }

  // Réinitialise les filtres quand la recherche est actualisée.
  // On observe l'objet data car celui-ci change à chaque fois que la recherche est actualisée.
  // Il n'est pas utile d'observer les champs de l'objet data vu que tout l'objet change.
  $effect(() => {
    data;
    if (untrack(() => filtersInitialized)) {
      resetFilters();
    } else {
      untrack(() => {
        filtersInitialized = true;
      });
    }
  });

  // Filtre les services en fonctions des filtres sélectionnés
  let filteredServices = $derived(
    data.services.filter((service) => {
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
    })
  );

  // Met à jour les paramètres d'URL en fonction des filtres sélectionnés
  $effect(() => {
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
  });

  let showDeploymentNotice = $derived(
    filteredServices.length < 10 &&
      !!data.cityCode &&
      !!data.servicesOptions &&
      !isInDeploymentDepartments(data.cityCode, data.servicesOptions)
  );

  let showMesAidesDialog = $derived(
    !$userInfo && data.categoryIds.includes("mobilite")
  );
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
            bind:currentPageLength
          />
        </div>
      {:else if showDeploymentNotice}
        <div class="mt-s24">
          <DoraDeploymentNotice />
        </div>
      {/if}
    </div>
  </div>
</CenteredGrid>

{#if showMesAidesDialog}
  <MesAidesDialog />
{/if}

<MonRecapPopup />
