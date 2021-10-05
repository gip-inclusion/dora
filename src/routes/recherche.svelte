<script context="module">
  export const ssr = false;
  import { getServicesOptions } from "$lib/services";
  import { getApiURL } from "$lib/utils/api.js";
  import { getQuery } from "./_homepage/_search";

  async function getResults(category, subcategory, cityCode) {
    const url = `${getApiURL()}/search/?${getQuery(
      category,
      subcategory,
      cityCode
    )}`;
    const res = await fetch(url, {
      headers: {
        Accept: "application/json; version=1.0",
      },
    });
    if (res.ok) {
      return await res.json();
    }
    // TODO: log errors
    try {
      console.error(await res.json());
    } catch (err) {
      console.error(err);
    }
    return [];
  }

  export async function load({ page, _fetch, _session, _context }) {
    const category = page.query.get("cat");
    const subcategory = page.query.get("sub");
    const cityCode = page.query.get("city");
    const cityLabel = page.query.get("cl");

    return {
      props: {
        category,
        subcategory,
        cityCode,
        cityLabel,
        results: await getResults(category, subcategory, cityCode),
        servicesOptions: await getServicesOptions(),
      },
    };
  }
</script>

<script>
  import { onMount } from "svelte";
  import { browser } from "$app/env";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  import SearchResult from "./_homepage/_search-result.svelte";
  import SearchTweakForm from "./_homepage/_search_tweak_form.svelte";

  import SearchPromo from "./_homepage/_search-promo.svelte";

  import { addCircleIcon } from "$lib/icons";
  import NoResultsPic from "$lib/assets/illu_zero-resultats-optimise.svg";
  import Button from "$lib/components/button.svelte";

  export let servicesOptions;
  export let category, subcategory, cityCode, cityLabel;
  export let results;

  onMount(() => {
    if (browser) {
      plausible("recherche", {
        props: { category, subcategory, cityCode, cityLabel },
      });
    }
  });
</script>

<style>
  .search-form {
    padding-top: var(--s56);
    grid-column: 1 / 5;
  }

  .results-wrapper {
    padding-bottom: var(--s56);
    grid-column: 5 / -1;
  }

  .results {
    display: flex;
    flex-direction: column;
    padding-top: var(--s56);
    padding-bottom: var(--s16);
    gap: var(--s16);
    grid-column: 5 / -1;
  }

  .no-results-wrapper {
    display: flex;
    flex-direction: row;
    padding-bottom: var(--s24);
    color: var(--col-text);
    gap: var(--s56);
  }

  .no-results {
    display: flex;
    flex-direction: column;
    padding-top: var(--s56);
    gap: var(--s16);
    grid-column: 6 / -2;
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
      bind:cityLabel
      {servicesOptions} />
  </div>
  <div class="results-wrapper">
    {#if results.length}
      <div class="results">
        {#each results as result}
          <SearchResult {result} />
        {/each}
      </div>
    {:else}
      <div class="no-results-wrapper">
        <img src={NoResultsPic} width="312" height="269" alt="" />
        <div class="no-results">
          <h2>Ooopsie !</h2>

          <p class="text-base">
            Aucun résultat ne correspond à vos critères 😞<br />
            Essayez d’affiner votre recherche.
          </p>
          <p class="text-sm">
            Le service DORA est actuellement
            <a
              class="underline"
              target="_blank"
              rel="noopener"
              href="https://beta.gouv.fr/startups/dora.html">
              en construction
            </a>, et se concentre sur 3 thématiques de services (mobilité, garde
            d’enfant et hébergement/logement) et 3 territoires
            (Loire-Atlantique, Ardennes et La Réunion).
          </p>

          <h4 class="mt-6">
            Vous connaissez des structures proposant des services correspondant
            à ces critères ? Invitez vos partenaires à se référencer :
          </h4>
          <div>
            <Button
              label="Recommander DORA"
              icon={addCircleIcon}
              disabled
              iconOnRight />
          </div>
          <h4>
            Vous êtes une structure proposant des services correspondant à ces
            critères ?
          </h4>
          <div>
            <LinkButton
              label="Référencer un service"
              icon={addCircleIcon}
              to={`/services/creer`}
              iconOnRight />
          </div>
        </div>
      </div>
    {/if}
    {#if category === "CC"}
      <SearchPromo />
    {/if}
  </div>
</CenteredGrid>
