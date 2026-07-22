<script lang="ts">
  import { beforeNavigate, goto } from "$app/navigation";
  import { page } from "$app/state";
  import Alert from "$lib/components/display/alert.svelte";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import Pagination from "$lib/components/display/pagination.svelte";
  import Spinner from "$lib/components/display/spinner.svelte";
  import {
    default as SearchFormByKeyword,
    ADDRESS_QUERY_PARAMS,
  } from "$lib/components/specialized/service-search-keyword.svelte";
  import { onMount } from "svelte";

  import type { PageData } from "./$types";
  import MapViewButton from "./map-view-button.svelte";
  import AddService from "./add-service.svelte";
  import ResultFilters, { type Filters } from "./result-filters.svelte";
  import SearchResults from "./search-results.svelte";
  import { trackKeywordSearch } from "$lib/utils/stats";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
  let fetchError = $derived(data.fetchError);
  let services = $derived(data.services);
  let pages = $derived(data.servicesPages);
  let total = $derived(data.servicesTotal);
  let loading = $state(false);
  let resultsTop = $state<HTMLDivElement>();

  // Variante mots-clés : mêmes filtres que le contrôle + le filtre
  // « Thématiques et besoins » (`categories`) et page.
  // Voir result-filters.svelte.
  const FILTER_KEY_TO_QUERY_PARAM: Record<keyof Filters, string> = {
    categories: "cats",
    subCategories: "subs",
    diPublics: "publics",
    kinds: "types",
    feeConditions: "frais",
    locationKinds: "modes_accueil",
  };

  const resetFiltersQueryParams = ["q", ...ADDRESS_QUERY_PARAMS];

  let searchId: number | null = $state(null);
  const pageFromURL: string | null = page.url.searchParams.get("page");
  let currentPage: number = $state(pageFromURL ? parseInt(pageFromURL) : 1);

  function filtersFromSearchParams(url: URL) {
    return (
      Object.entries(FILTER_KEY_TO_QUERY_PARAM) as [keyof Filters, string][]
    ).reduce<Filters>(
      (acc, [filterKey, queryParam]) => ({
        ...acc,
        [filterKey]: url.searchParams.getAll(queryParam),
      }),
      {} as Filters
    );
  }

  let filters = $state(filtersFromSearchParams(page.url));

  async function trackSearch() {
    // Le tracking doit être comparable à la recherche historique. Cela
    // implique un suivi imparfait des actions de l’utilisateur.
    const cityCode = page.url.searchParams.get("code_commune") ?? "";
    const categoryIds = page.url.searchParams.getAll("cats");
    const subCategoryIds = page.url.searchParams.getAll("subs");
    const kinds = page.url.searchParams.getAll("types");
    const feeConditions = page.url.searchParams.getAll("frais");
    const locationKinds = page.url.searchParams.getAll("modes_accueil");
    const keywords = page.url.searchParams.get("q") || "";
    searchId = await trackKeywordSearch(
      page.url,
      keywords,
      cityCode,
      categoryIds,
      subCategoryIds,
      kinds,
      feeConditions,
      locationKinds,
      services,
      total,
      fetch
    );
  }

  function navigate(url: URL) {
    loading = true;
    goto(url, {
      keepFocus: true,
      noScroll: true,
    }).then(() => {
      loading = false;
    });
  }

  function gotoPage(newPage: number) {
    currentPage = newPage;
    const url = new URL(page.url);
    if (newPage === 1) {
      url.searchParams.delete("page");
    } else {
      url.searchParams.set("page", newPage.toString());
    }
    navigate(url);
  }

  function normalizeQueryParams(searchParams: URLSearchParams): string {
    const copy = new URLSearchParams(searchParams);
    copy.delete("page");
    copy.sort();
    return copy.toString();
  }

  beforeNavigate(({ from, to }) => {
    if (!from || !to || from.route.id !== to.route.id) {
      return;
    }
    for (const key of resetFiltersQueryParams) {
      if (from.url.searchParams.get(key) !== to.url.searchParams.get(key)) {
        filters = filtersFromSearchParams(to.url);
        trackSearch();
        return;
      }
    }
  });

  $effect(() => {
    const url = new URL(page.url);
    Object.entries(filters).forEach(([filterKey, value]) => {
      const queryParam = FILTER_KEY_TO_QUERY_PARAM[filterKey as keyof Filters];
      url.searchParams.delete(queryParam);
      for (const param of value) {
        url.searchParams.append(queryParam, param);
      }
    });
    if (
      normalizeQueryParams(url.searchParams) !==
      normalizeQueryParams(page.url.searchParams)
    ) {
      currentPage = 1;
      url.searchParams.delete("page");
      navigate(url);
    }
  });

  onMount(trackSearch);
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
        {services}
        {total}
        {pages}
        {searchId}
        current={currentPage}
        onPageChange={gotoPage}
      />
      <ResultFilters servicesOptions={data.servicesOptions} bind:filters />
    </div>
    {#if fetchError}
      <Alert id="results-fetch-error" label={fetchError} />
    {:else}
      <div bind:this={resultsTop} class="lg:basis-2/3">
        <Notice
          type="info"
          title="Comment les services sont-ils filtrés ?"
          titleLevel="h3"
        >
          <span>
            <strong>
              {new Intl.NumberFormat().format(total)}
              {total > 1 ? "résultats triés" : "résultat trié"}
              par pertinence
            </strong>. Vos mots-clés sont recherchés parmi les noms, les
            thématiques, les publics et les descriptions des services.
          </span>
        </Notice>

        <div class="mt-s32">
          {#if loading}
            <div class="flex items-center">
              <Spinner size="40px" />
              <span class="mx-s16">Chargement…</span>
            </div>
          {:else}
            {#if total}
              <SearchResults {searchId} {services} />
              <Pagination
                current={currentPage}
                totalPages={pages}
                onPageChange={(activePage) => {
                  resultsTop?.scrollIntoView();
                  gotoPage(activePage);
                }}
              />
            {/if}
            <div class="mt-s16">
              <AddService />
            </div>
          {/if}
        </div>
      </div>
    {/if}
  </div>
</CenteredGrid>
