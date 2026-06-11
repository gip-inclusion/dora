<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/state";
  import Alert from "$lib/components/display/alert.svelte";
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
  let fetchError = $derived(data.fetchError);
  let services = $derived(data.services);
  let pages = $derived(data.servicesPages);
  let total = $derived(data.servicesTotal);
  let loading = $state(false);
  let resultsTop;

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

  let filters = $state(
    (
      Object.entries(FILTER_KEY_TO_QUERY_PARAM) as [keyof Filters, string][]
    ).reduce<Filters>(
      (acc, [filterKey, queryParam]) => ({
        ...acc,
        [filterKey]: page.url.searchParams.getAll(
          decodeURIComponent(queryParam)
        ),
      }),
      {} as Filters
    )
  );
  const pageFromURL: string | null = page.url.searchParams.get("page");
  let currentPage: number = $state(pageFromURL ? parseInt(pageFromURL) : 1);

  function setPage(newPage: number) {
    currentPage = newPage;
    if (currentPage === 1) {
      page.url.searchParams.delete("page");
    } else {
      page.url.searchParams.set("page", currentPage.toString());
    }
  }

  function refreshResults() {
    loading = true;
    goto(page.url, {
      state: page.url.searchParams.toString(),
      keepFocus: true,
      noScroll: true,
      // TODO: Can Svelte be smart enough to invalidate that cache on its own?
      invalidate: [(url: URL): boolean => url.pathname === SEARCH_KEYWORD_URL],
    }).then(() => {
      loading = false;
    });
  }

  function normalizeQueryParams(searchParams: URLSearchParams): string {
    const copy = new URLSearchParams(searchParams);
    copy.delete("page");
    copy.sort();
    return copy.toString();
  }
  $effect(() => {
    const before = normalizeQueryParams(page.url.searchParams);
    Object.entries(filters).forEach(([filterKey, value]) => {
      const queryParam = FILTER_KEY_TO_QUERY_PARAM[filterKey];
      page.url.searchParams.delete(queryParam);
      for (const param of value) {
        page.url.searchParams.append(queryParam, encodeURIComponent(param));
      }
    });
    if (before !== normalizeQueryParams(page.url.searchParams)) {
      setPage(1);
      refreshResults();
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

    <SearchFormByKeyword
      onSearch={() => {
        filters = (
          Object.entries(FILTER_KEY_TO_QUERY_PARAM) as [keyof Filters, string][]
        ).reduce(
          (acc, [key, _value]) => ({ ...acc, [key]: [] }),
          {} as Filters
        );
        setPage(1);
      }}
    />
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
    {#if fetchError}
      <Alert id="results-fetch-error" label={fetchError} />
    {:else}
      <div bind:this={resultsTop} class="lg:basis-2/3">
        <Notice
          type="info"
          title="Comment les services sont-ils filtrés ?"
          titleLevel="h3"
        >
          <span>
            <strong>
              {total}
              {total > 1 ? "services" : "service"}
            </strong>
            {#if data.keywords}
              {total > 1 ? "contiennent" : "contient"}
              le mot-clé « <strong>{data.keywords}</strong> » en titre, description,
              type de structure, thématique, public
            {/if}
            {#if page.url.searchParams.get("label")}
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
                current={currentPage}
                totalPages={pages}
                onPageChange={(activePage) => {
                  setPage(activePage);
                  resultsTop.scrollIntoView();
                  refreshResults();
                }}
              />
            {/if}

            <NoResultCard />
          {/if}
        </div>
      </div>
    {/if}
  </div></CenteredGrid
>
