<script>
  import { onMount } from "svelte";

  import { page } from "$app/stores";
  import { getApiURL } from "$lib/utils";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import SearchResult from "./_homepage/_search-result.svelte";

  const category = $page.query.get("cat");
  const subcategory = $page.query.get("sub");
  const cityCode = $page.query.get("city");

  let results = [];

  async function getResults() {
    const url = `${getApiURL()}/search/?cat=${category}&sub=${subcategory}&city=${cityCode}`;
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

  onMount(async () => {
    results = (await getResults()).result;
    console.log(results);
  });
</script>

<style>
  .wrapper {
    display: flex;
    flex-direction: column;
    padding-top: 40px;
    gap: var(--s16);
    grid-column: 1 / -1;
  }
</style>

<CenteredGrid>
  <div class="col-start-1 col-span-full text-center mb-6">
    <p class="text-gray-text text-base">Consultez les offres</p>
    <h1 class="text-france-blue text-13xl">Résultats de recherche</h1>
  </div>
</CenteredGrid>

<CenteredGrid gridRow="2" roundedbg>
  <div class="wrapper">
    {#each results as result}
      <SearchResult {result} />
    {/each}
  </div>
</CenteredGrid>
