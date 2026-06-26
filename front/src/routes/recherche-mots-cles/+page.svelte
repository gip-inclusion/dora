<script lang="ts">
  import { tick, untrack } from "svelte";
  import { browser } from "$app/environment";

  import { page } from "$app/stores";

  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import SearchFormByKeyword from "$lib/components/specialized/service-search-keyword.svelte";

  import type { PageData } from "./$types";
  import MapViewButton from "./map-view-button.svelte";
  import NoResultCard from "./no-result-card.svelte";
  import ResultFilters, { type Filters } from "./result-filters.svelte";
  import SearchResults, {
    SEARCH_RESULTS_PAGE_LENGTH,
  } from "./search-results.svelte";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  interface SnapshotState {
    scrollY: number;
    filters: Filters;
    currentPageLength: number;
  }

  // Variante mots-clés : mêmes filtres que le contrôle + le filtre
  // « Thématiques et besoins » (`categories`). Voir result-filters.svelte.
  const FILTER_KEY_TO_QUERY_PARAM: Record<keyof Filters, string> = {
    categories: "cats",
    diPublics: "publics",
    kinds: "kinds",
    fundingLabels: "funding",
    feeConditions: "fees",
    locationKinds: "locs",
  };

  let filtersInitialized = $state(false);

  let filters = $state(
    (
      Object.entries(FILTER_KEY_TO_QUERY_PARAM) as [keyof Filters, string][]
    ).reduce<Filters>(
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

  function resetFilters() {
    filters = {
      categories: [],
      diPublics: [],
      kinds: [],
      fundingLabels: [],
      feeConditions: [],
      locationKinds: [],
    };
    // Réinitialise aussi la pagination quand on change les filtres
    currentPageLength = SEARCH_RESULTS_PAGE_LENGTH;
  }

  // Réinitialise les filtres quand la recherche est actualisée.
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

  // Filtre les services en fonction des filtres sélectionnés.
  // Ici on n'exclut pas les services « à distance » : l'ordre renvoyé par le back est préservé.
  let filteredServices = $derived(
    // TODO(A/B mots-clés) : Se débrouiller pour relancer la recherche en passant les thématiques lors de l'utilisation du filtre ? Sauf si `thematiques` reste une propriété de service..?
    data.services.filter((service) => {
      const categoriesMatch =
        filters.categories.length === 0 ||
        (service.categories &&
          filters.categories.some((value) =>
            service.categories!.includes(value)
          ));
      const diPublicsMatch =
        filters.diPublics.length === 0 ||
        filters.diPublics.some((value) => service.diPublics.includes(value));
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

      return (
        categoriesMatch &&
        diPublicsMatch &&
        kindsMatch &&
        fundingLabelsMatch &&
        feeConditionMatch &&
        locationKindsMatch
      );
    })
  );

  // Met à jour les paramètres d'URL en fonction des filtres sélectionnés
  $effect(() => {
    (Object.keys(filters) as (keyof Filters)[]).forEach((filterKey) => {
      const queryParam = FILTER_KEY_TO_QUERY_PARAM[filterKey];
      if (filters[filterKey].length > 0) {
        $page.url.searchParams.set(queryParam, filters[filterKey].join(","));
      } else {
        $page.url.searchParams.delete(queryParam);
      }
    });
    window.history.replaceState(
      history.state,
      "",
      `?${$page.url.searchParams.toString()}`
    );
  });
</script>

<CenteredGrid bgColor="bg-blue-light">
  <div>
    <h1 class="sr-only">
      Résultats de votre recherche de services d’insertion par mots-clés
    </h1>

    <div class="mb-s24">
      <Breadcrumb currentLocation="search" />
    </div>

    <SearchFormByKeyword />
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
      <Notice
        type="info"
        title="Comment les services sont-ils filtrés ?"
        titleLevel="h3"
      >
        <span>
          <strong
            >{filteredServices.length}
            {filteredServices.length > 1 ? "services" : "service"}</strong
          >
          {#if data.keywords}
            {filteredServices.length > 1 ? "contiennent" : "contient"}
            le mot-clé « <strong>{data.keywords}</strong> » en titre, description,
            type de structure, thématique, public
          {/if}
          {#if true}
            à proximité de l'adresse sélectionnée. Les résultats sont classés
          {/if}
          par ordre de pertinence.
        </span>
      </Notice>

      {#if filteredServices.length}
        <div class="mt-s32">
          <SearchResults {data} {filteredServices} bind:currentPageLength />
        </div>
      {/if}

      <div class="mt-s32">
        <NoResultCard />
      </div>
    </div>
  </div>
</CenteredGrid>
