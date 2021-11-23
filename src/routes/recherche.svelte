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

  import { mailIcon, newspaperIcon } from "$lib/icons";
  import NoResultsPic from "$lib/assets/illu_zero-resultats-optimise.svg";

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
      {servicesOptions}
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
            Le service DORA est actuellement
            <a
              class="underline"
              target="_blank"
              rel="noopener"
              href="https://communaute.inclusion.beta.gouv.fr/t/mise-en-visibilite-de-loffre-dinsertion-lancement-de-dora/4090"
            >
              en construction
            </a>, et se concentre sur 3 thématiques de services (mobilité, garde
            d’enfant et hébergement/logement) et 3 territoires
            (Loire-Atlantique, Ardennes et La Réunion).
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
              to="https://itou.typeform.com/doraall"
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
