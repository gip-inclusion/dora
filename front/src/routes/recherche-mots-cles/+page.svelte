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
        [filterKey]: page.url.searchParams.getAll(queryParam),
      }),
      {} as Filters
    )
  );
  const pageFromURL: string | null = page.url.searchParams.get("page");
  let currentPage: number = $state(pageFromURL ? parseInt(pageFromURL) : 1);

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
    // On rajoute explicitement le `searchId` à l'URL afin de le conserver
    // d'une page à l'autre lors de la pagination.
    if (data.searchId) {
      url.searchParams.set("searchId", String(data.searchId));
    }
    navigate(url);
  }

  function normalizeQueryParams(searchParams: URLSearchParams): string {
    const copy = new URLSearchParams(searchParams);
    copy.delete("page");
    // `searchId` n'est pas un filtre/critère de recherche : on l'ignore dans
    // la comparaison afin que son ajout ne soit pas pris pour un changement de filtre.
    copy.delete("searchId");
    copy.sort();
    return copy.toString();
  }
  $effect(() => {
    const url = new URL(page.url);
    Object.entries(filters).forEach(([filterKey, value]) => {
      const queryParam = FILTER_KEY_TO_QUERY_PARAM[filterKey];
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
      // Un changement de filtre constitue en revanche une nouvelle recherche :
      // un nouvel événement `search` doit être émis (i.e. avec un nouveau `searchId`).
      url.searchParams.delete("searchId");
      navigate(url);
    }
  });

  // Une fois l'événement `search` émis (lors d'une nouvelle recherche), on
  // ajoute le `searchId` à l'URL afin qu'il soit conservé lors de la
  // pagination et du retour dans l'historique (notamment depuis la page d'un
  // service), et ce, sans re-déclencher de recherche.
  $effect(() => {
    if (data.searchId && !page.url.searchParams.get("searchId")) {
      const url = new URL(page.url);
      url.searchParams.set("searchId", String(data.searchId));
      window.history.replaceState(
        history.state,
        "",
        `${url.pathname}${url.search}`
      );
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
        currentPage = 1;
      }}
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
        {services}
        {total}
        {pages}
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
              <SearchResults {data} {services} />
              <Pagination
                current={currentPage}
                totalPages={pages}
                onPageChange={(activePage) => {
                  resultsTop.scrollIntoView();
                  gotoPage(activePage);
                }}
              />
            {/if}
            <div class="mt-s16">
              <NoResultCard />
            </div>
          {/if}
        </div>
      </div>
    {/if}
  </div></CenteredGrid
>
