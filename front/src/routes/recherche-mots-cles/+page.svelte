<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/state";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import Pagination from "$lib/components/display/pagination.svelte";
  import Spinner from "$lib/components/display/spinner.svelte";
  import SearchFormByKeyword from "$lib/components/specialized/service-search-keyword.svelte";
  import { SEARCH_KEYWORD_URL } from "$lib/consts";

  import type { PageData } from "./$types";
  import MapViewButton from "./map-view-button.svelte";
  import NoResultCard from "./no-result-card.svelte";
  import ResultFilters, { type Filters } from "./result-filters.svelte";
  import SearchResults from "./search-results.svelte";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
  let services = $derived(data.services);
  let pageSize = $derived(data.servicesPageSize);
  let total = $derived(data.servicesTotal);
  let loading = $state(false);
  let resultsTop;

  // Variante mots-clés : mêmes filtres que le contrôle + le filtre
  // « Thématiques et besoins » (`categories`) et page.
  // Voir result-filters.svelte.
  const FILTER_KEY_TO_QUERY_PARAM: Record<keyof Filters, string> = {
    categories: "cats",
    diPublics: "publics",
    kinds: "types",
    fundingLabels: "funding",
    feeConditions: "frais",
    locationKinds: "modes_accueil",
    page: "page",
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

  $effect(() => {
    const before = new URLSearchParams(page.url.searchParams);
    Object.entries(filters).forEach(([filterKey, value]) => {
      const queryParam = FILTER_KEY_TO_QUERY_PARAM[filterKey];
      page.url.searchParams.delete(queryParam);
      for (const param of value) {
        page.url.searchParams.append(queryParam, param);
      }
    });
    if (page.url.searchParams.toString() !== before.toString()) {
      loading = true;
      if (page.url.searchParams.get("page") === before.get("page")) {
        filters.page = [1];
      }
      goto(page.url, {
        state: page.url.searchParams.toString(),
        keepFocus: true,
        noScroll: true,
        invalidate: [
          (url: URL): boolean => {
            return url.pathname === SEARCH_KEYWORD_URL;
          },
        ],
      }).then(() => {
        loading = false;
      });
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
      <MapViewButton {data} bind:filters {services} {total} />
      <ResultFilters servicesOptions={data.servicesOptions} bind:filters />
    </div>
    <div bind:this={resultsTop}>
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

        <div class="mt-s32">
          {#if loading}
            <div class="flex items-center">
              <Spinner size="40px" />
              <span class="mx-s16">Chargement…</span>
            </div>
          {:else}
            {#if total}
              <SearchResults {data} {services} />
              <Pagination
                // TODO: page should not be an array.
                current={parseInt(filters.page[0]) || 1}
                totalPages={Math.ceil(total / pageSize)}
                onPageChange={(activePage) => {
                  filters.page = [activePage];
                  resultsTop.scrollIntoView();
                }}
              />
            {/if}

            <NoResultCard />
          {/if}
        </div>
      </div>
    </div>
  </div></CenteredGrid
>
