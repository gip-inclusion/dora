<script lang="ts">
  import { page } from "$app/stores";

  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import SearchForm from "$lib/components/specialized/service-search.svelte";
  import type { ServiceSearchResult } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { isInDeploymentDepartments } from "$lib/utils/misc";

  import type { PageData } from "./$types";
  import DoraDeploymentNotice from "./dora-deployment-notice.svelte";
  import OnlyNationalResultsNotice from "./only-national-results-notice.svelte";
  import ServiceSuggestionNotice from "./service-suggestion-notice.svelte";
  import ResultFilters, { type Filters } from "./result-filters.svelte";
  import MapViewButton from "./map-view-button.svelte";
  import ResultCount from "./result-count.svelte";
  import SearchResults from "./search-results.svelte";
  import MesAidesDialog from "./mes-aides-dialog.svelte";

  export let data: PageData;

  const FILTER_KEY_TO_QUERY_PARAM = {
    kinds: "kinds",
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

  function resetFilters() {
    filters = { kinds: [], feeConditions: [], locationKinds: [] };
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
      kindsMatch && feeConditionMatch && locationKindsMatch && onSiteAndNearby
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

  function hasOnlyNationalResults(services: ServiceSearchResult[]) {
    if (services.length === 0) {
      return false;
    }
    return services.every((service) => service.diffusionZoneType === "country");
  }

  $: showDeploymentNotice =
    data.cityCode &&
    !isInDeploymentDepartments(data.cityCode, data.servicesOptions);

  $: showMesAidesDialog = !$userInfo && data.categoryIds.includes("mobilite");
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

<CenteredGrid extraClass="m-auto">
  <div class="lg:flex lg:flex-row lg:items-start lg:gap-s24">
    <div
      class="hidden flex-col gap-s32 rounded-ml border border-gray-02 p-s32 shadow-sm lg:flex lg:basis-1/3"
    >
      <MapViewButton {data} bind:filters {filteredServices} />
      <ResultFilters servicesOptions={data.servicesOptions} bind:filters />
    </div>
    <div class="lg:basis-2/3">
      <div class="mt-s16 text-f21">
        <ResultCount
          resultCount={filteredServices.length}
          cityLabel={data.cityLabel}
        />
      </div>

      {#if showDeploymentNotice}
        <div class="mt-s24">
          <DoraDeploymentNotice />
        </div>
      {/if}

      {#if hasOnlyNationalResults(filteredServices)}
        <div class="mt-s24">
          <OnlyNationalResultsNotice />
        </div>
      {/if}

      {#if filteredServices.length}
        <div class="mt-s32">
          <SearchResults {data} {filters} {filteredServices} />
        </div>
      {/if}

      <div class="mb-s24 mt-s48 lg:flex lg:gap-s24">
        <ServiceSuggestionNotice />
      </div>
    </div>
  </div>
</CenteredGrid>

{#if showMesAidesDialog}
  <MesAidesDialog />
{/if}
