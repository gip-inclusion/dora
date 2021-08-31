<script context="module">
  import { getServicesOptions } from "$lib/services";

  export async function load({ _page, _fetch, _session, _context }) {
    return {
      props: {
        servicesOptions: await getServicesOptions(),
      },
    };
  }
</script>

<script>
  import { page } from "$app/stores";
  import { getApiURL } from "$lib/utils";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import SearchResult from "./_homepage/_search-result.svelte";
  import SearchTweakForm from "./_homepage/_search_tweak_form.svelte";

  let category = $page.query.get("cat");
  let subcategory = $page.query.get("sub");
  let cityCode = $page.query.get("city");
  export let servicesOptions;
  let results = [];

  async function getResults() {
    let url = `${getApiURL()}/search/?cat=${category}&city=${cityCode}`;
    if (subcategory != null) url += `&subcat=${subcategory}`;
    const res = await fetch(url, {
      headers: {
        Accept: "application/json; version=1.0",
      },
    });

    const result = {
      ok: res.ok,
      status: res.status,
    };
    if (res.ok) {
      result.result = await res.json();
    } else {
      try {
        result.error = await res.json();
      } catch (err) {
        console.error(err);
      }
    }
    return result;
  }

  async function updateResults() {
    results = (await getResults()).result;
  }

  // eslint-disable-next-line
  $: $page.query, updateResults();
</script>

<style>
  .search-form {
    padding-top: var(--s56);
    grid-column: 1 / 5;
  }

  .results {
    display: flex;
    flex-direction: column;
    padding-top: var(--s56);
    gap: var(--s16);
    grid-column: 5 / -1;
  }
</style>

<CenteredGrid>
  <div class="col-start-1 col-span-full text-center mb-6">
    <p class="text-gray-text text-base">Consultez les services</p>
    <h1 class="text-france-blue text-13xl">Résultats de recherche</h1>
  </div>
</CenteredGrid>

<CenteredGrid gridRow="2" roundedbg>
  <div class="search-form">
    <SearchTweakForm
      numResults={results.length}
      bind:category
      bind:subcategory
      bind:cityCode
      {servicesOptions} />
  </div>
  <div class="results">
    {#each results as result}
      <SearchResult {result} />
    {/each}
  </div>
</CenteredGrid>
