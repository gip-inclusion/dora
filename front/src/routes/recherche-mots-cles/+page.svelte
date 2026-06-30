<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/state";
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
  let services = $derived(data.services);
  let total = $derived(data.servicesTotal);

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

  let filters = $state(
    (
      Object.entries(FILTER_KEY_TO_QUERY_PARAM) as [keyof Filters, string][]
    ).reduce<Filters>(
      (acc, [filterKey, queryParam]) => ({
        ...acc,
        [filterKey]: page.url.searchParams.getAll(queryParam),
      }),
      {} as Filters
    )
  );
  let currentPageLength = $state(SEARCH_RESULTS_PAGE_LENGTH);

  $effect(() => {
    const before = page.url.searchParams.toString();
    console.log("BEFORE", before);
    Object.entries(filters).forEach(([filterKey, value]) => {
      const queryParam = FILTER_KEY_TO_QUERY_PARAM[filterKey];
      page.url.searchParams.delete(queryParam);
      for (const param of value) {
        page.url.searchParams.append(queryParam, param);
      }
    });
    console.log("AFTER", page.url.searchParams.toString());
    if (page.url.searchParams.toString() !== before) {
      console.log(`Should load ${page.url}`);
      goto(page.url, {
        noScroll: true,
        keepFocus: true,
        state: page.url.searchParams.toString(),
      });
    } else {
      console.log("Skipping load");
    }
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
        {services}
        {total}
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
            >{total}
            {total > 1 ? "services" : "service"}</strong
          >
          {#if data.keywords}
            {total > 1 ? "contiennent" : "contient"}
            le mot-clé « <strong>{data.keywords}</strong> » en titre, description,
            type de structure, thématique, public
          {/if}
          {#if true}
            à proximité de l'adresse sélectionnée. Les résultats sont classés
          {/if}
          par ordre de pertinence.
        </span>
      </Notice>

      {#if total}
        <div class="mt-s32">
          <SearchResults {data} {services} bind:currentPageLength {total} />
        </div>
      {/if}

      <div class="mt-s32">
        <NoResultCard />
      </div>
    </div>
  </div>
</CenteredGrid>
