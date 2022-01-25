<script context="module">
  import { getServicesOptions } from "$lib/services";
  import { getApiURL } from "$lib/utils/api.js";
  import { getQuery } from "./_homepage/_search";

  async function getResults(category, subcategory, cityCode, radius) {
    const url = `${getApiURL()}/search/?${getQuery(
      category,
      subcategory,
      cityCode,
      radius
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

  const radiusChoices = [
    { value: "10", label: "10 km" },
    { value: "20", label: "20 km" },
    { value: "50", label: "50 km" },
    { value: "100", label: "100 km" },
  ];

  export async function load({ url }) {
    const query = url.searchParams;
    const category = query.get("cat");
    const subcategory = query.get("sub");
    const cityCode = query.get("city");
    const cityLabel = query.get("cl");
    const radius = query.get("radius") || radiusChoices[0].value;

    return {
      props: {
        category,
        subcategory,
        cityCode,
        cityLabel,
        radius,
        results: await getResults(category, subcategory, cityCode, radius),
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

  import { mailIcon, newspaperIcon } from "$lib/icons";
  import NoResultsPic from "$lib/assets/illu_zero-resultats-optimise.svg";

  export let servicesOptions;
  export let category, subcategory, cityCode, cityLabel, radius;
  export let results;

  onMount(() => {
    if (browser) {
      plausible("recherche", {
        props: { category, subcategory, cityCode, cityLabel },
      });
    }
  });

  const sharingEmailSubject = encodeURIComponent("Connaissez-vous Dora ?");
  const sharingEmailBody = encodeURIComponent(
    `
Bonjour,
Je me permets de vous partager un projet qui devrait vous intéresser.

Connaissez-vous Dora ?

Lancé en Mai 2021, Dora est un service public numérique porté par la DGEFP qui permet aux structures de l'insertion de référencer simplement et mettre à jour en temps réel leur offre de services, et aux professionnels prescripteurs de rechercher et mobiliser rapidement le service le plus adapté au besoin de leur bénéficiaire.

J'ai le plaisir de vous annoncer que Dora est accessible dès aujourd'hui pour l'ensemble les acteurs de l'insertion du territoire. De nombreux partenaires ont d'ores et déjà mis en visibilité leur offre de service sur Dora. Vous pouvez également vous inscrire et bénéficier de ce service !

👉 Pour accéder à Dora cliquez sur ce lien (pensez à l'ajouter à vos favoris 😉) :
https://dora.fabrique.social.gouv.fr/

Dans l'attente de pouvoir consulter votre offre de service sur cet outil.
Cordialement,
`.trim()
  );
</script>

<svelte:head>
  <title>Résultats de recherche | DORA</title>
</svelte:head>

<CenteredGrid topPadded>
  <div class="col-start-1 col-span-full text-center mb-s48">
    <p class="text-f16">Consultez les services</p>
    <h1 class="text-france-blue">Résultats de recherche</h1>
  </div>
</CenteredGrid>

<CenteredGrid roundedbg>
  <div class="search-form">
    <SearchTweakForm
      numResults={results.length}
      bind:category
      bind:subcategory
      bind:cityCode
      bind:cityLabel
      bind:radius
      {servicesOptions}
      {radiusChoices}
    />
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
        <img
          src={NoResultsPic}
          width="312"
          height="269"
          alt=""
          class="self-center"
        />
        <div class="no-results">
          <h2>Ooopsie !</h2>

          <p class="text-f16">
            Aucun résultat ne correspond à vos critères 😞<br />
            Essayez d’affiner votre recherche.
          </p>
          <p class="text-f14">
            Les premiers départements accessibles à la recherche sont les
            Ardennes et l’Ile de la Réunion.
            <a
              class="underline"
              target="_blank"
              rel="noopener"
              href="https://documentation.dora.fabrique.social.gouv.fr/le-projet-dora/lancement-du-projet-dora/acceleration-de-dora-des-octobre-2021"
            >
              Suivez l’ouverture des autres territoires</a
            >.
          </p>

          <h4 class="mt-s48">
            Vous connaissez des structures proposant des services correspondant
            à ces critères ? Invitez vos partenaires à se référencer :
          </h4>
          <div>
            <LinkButton
              label="Recommander DORA"
              icon={mailIcon}
              iconOnRight
              to="mailto:?subject={sharingEmailSubject}&body={sharingEmailBody}"
            />
          </div>
          <h4 class="mt-s48">
            Infolettre : nouveautés et les prochains territoires ouverts sur
            Dora.
          </h4>
          <div>
            <LinkButton
              label="Recevoir les actualités"
              icon={newspaperIcon}
              iconOnRight
              to="https://d4c653e7.sibforms.com/serve/MUIEAEkY4naptXBIq5NdRg5UPxP1wmwbGCinne5c1gynY-wfrZ0Dz0QP_NqkXtfyYqhdaq3AO8VFZJ9giRi9ZT0eah7Ut2U0LeKSTVIHQb_5nhvTLUMWXo9ZMeIYCHVlzmjkXGQ66S5ewcYpSADUgV--2RVZ_mrnsRJQoCNwZ8y-sWzfQsEzfKuTA7SLbZ_dWeqaigudym3EaiHT"
              otherTab
              nofollow
            />
          </div>
        </div>
      </div>
    {/if}
    {#if category === "CC"}
      <SearchPromo />
    {/if}
  </div>
</CenteredGrid>

<style lang="postcss">
  .search-form {
    padding-top: var(--s56);
    grid-column: 1 / -1;
  }

  .results-wrapper {
    padding-bottom: var(--s56);
    grid-column: 1 / -1;
  }

  .results {
    display: flex;
    flex-direction: column;
    padding-top: var(--s56);
    padding-bottom: var(--s16);
    gap: var(--s16);
  }

  .no-results-wrapper {
    display: flex;
    flex-direction: column;
    padding-top: var(--s56);
    padding-bottom: var(--s24);
    color: var(--col-text);
    gap: var(--s56);
  }

  .no-results {
    display: flex;
    flex-direction: column;
    gap: var(--s16);
  }

  @screen xl {
    .no-results-wrapper {
      flex-direction: row;
    }
  }

  @screen lg {
    .search-form {
      padding-top: var(--s56);
      grid-column: 1 / 5;
    }

    .results-wrapper {
      grid-column: 5 / -1;
    }
  }
</style>
