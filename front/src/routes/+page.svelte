<script lang="ts">
  import PlayCircleFillMedia from "svelte-remix/PlayCircleFillMedia.svelte";

  import illuAccompagner from "$lib/assets/illustrations/illu-accompagner.svg";
  import illuMobiliser from "$lib/assets/illustrations/illu-mobiliser.svg";
  import illuRecenser from "$lib/assets/illustrations/illu-recenser.svg";
  import logoDataInclusion from "$lib/assets/logos/logo-data-inclusion.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import ExternalLinkIcon from "$lib/components/display/external-link-icon.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Tabs from "$lib/components/display/tabs.svelte";
  import PartnerList from "$lib/components/specialized/partner-list.svelte";
  import SearchForm from "$lib/components/specialized/service-search.svelte";
  import SearchFormByKeyword from "$lib/components/specialized/service-search-keyword.svelte";
  import { GOOGLE_CSE_ID, INCLUSION_PLATFORM_URL } from "$lib/env";
  import { refreshUserInfo, userInfo } from "$lib/utils/auth";
  import { registerRechercheTextuelleExperiment } from "$lib/utils/matomo";
  import { userPreferences } from "$lib/utils/preferences";
  import ServicesToUpdateNotice from "./structures/[slug]/services/services-to-update-notice.svelte";
  import MonRecapPopup from "$lib/components/specialized/mon-recap-popup.svelte";
  import { getCurrentlySelectedStructure } from "$lib/utils/current-structure";

  import { page } from "$app/state";
  import type { PageData } from "./$types";
  import { URL_HELP_SITE } from "$lib/consts";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  const homeTabs = [
    { id: "accompagnement", name: "Professionnels de l’accompagnement" },
    { id: "porteurs", name: "Porteurs de services" },
    { id: "particuliers", name: "Particuliers" },
  ];
  let selectedTabId = $state("accompagnement");

  let lastVisitedStructure = $derived(
    getCurrentlySelectedStructure($userInfo, $userPreferences)
  );

  // Afin de faciliter certaines démonstrations, il est possible d'activer la
  // recherche par mots-clés / texte libre via le paramètre d'URL `searchByText`.
  const searchByTextParam = $derived.by(() => {
    const v = page.url.searchParams.get("searchByText");
    if (v === "1") {
      return true;
    }
    if (v === "0") {
      return false;
    }
    return null;
  });
  let searchByTextMatomo = $state(false);
  registerRechercheTextuelleExperiment(() => {
    searchByTextMatomo = true;
  });
  const searchByText = $derived(searchByTextParam ?? searchByTextMatomo);
</script>

<CenteredGrid extraClass="pt-s32" bgColor="bg-magenta-10" noPadding>
  <h1 class="mb-s32 text-france-blue m-auto text-center text-balance">
    Trouvez le service adapté<br />pour lever les freins à l’insertion
  </h1>

  {#if searchByText}
    <div class="mb-s16">
      <SearchFormByKeyword />
    </div>
  {:else}
    <SearchForm
      servicesOptions={data.servicesOptions}
      cityCode={data.cityCode}
      cityLabel={data.cityLabel}
      label={data.cityLabel}
      initialSearch
    />
    {#if GOOGLE_CSE_ID}
      <div class="mt-s32 flex items-center justify-center">
        <div class="mr-s16">ou</div>
        <LinkButton
          label="Faire une recherche par mots-clés"
          to={`/recherche-textuelle`}
        />
      </div>
    {/if}
  {/if}

  {#if lastVisitedStructure?.canEditInformations}
    <div class="mt-s32">
      <ServicesToUpdateNotice
        structureSlug={lastVisitedStructure.slug}
        servicesToUpdate={lastVisitedStructure.servicesToUpdate}
        onRefresh={refreshUserInfo}
      />
    </div>
  {/if}

  <div class="mt-s32">
    <Tabs
      items={homeTabs}
      itemId={selectedTabId}
      onSelectedChange={(id) => (selectedTabId = id)}
    />
  </div>
</CenteredGrid>

<CenteredGrid roundedColor="bg-magenta-10">
  <div
    class="mb-s32 gap-s24 flex flex-col md:flex-row md:justify-center"
    role="tabpanel"
    aria-labelledby={`tab-${selectedTabId}`}
  >
    {#if selectedTabId === "accompagnement"}
      <div class="md:basis-1/3">
        <img src={illuRecenser} alt="" class="mb-s16 w-full" />
        <h3 class="text-france-blue">Identifiez des services</h3>
        <p class="text-f16">
          DORA vous permet d’<strong
            >identifier les services d’insertion les plus adaptés</strong
          >
          aux besoins spécifiques de vos bénéficiaires.
        </p>
      </div>
      <div class="md:basis-1/3">
        <img src={illuAccompagner} alt="" class="mb-s16 w-full" />
        <h3 class="text-france-blue">Orientez vos bénéficiaires</h3>
        <p class="text-f16">
          Le formulaire <strong
            >facilite l’orientation de vos bénéficiaires</strong
          >
          vers la solution identifiée. Il est maintenant intégré directement à la
          Plateforme de l’inclusion.
        </p>
        <a
          href={`${INCLUSION_PLATFORM_URL}/search/services?mtm_campaign=DORA&mtm_kwd=homeorienter`}
          target="_blank"
          rel="noopener"
          class="text-f14 text-magenta-cta font-bold"
        >
          Orientez votre bénéficiaire<ExternalLinkIcon />
        </a>
      </div>
      <div class="md:basis-1/3">
        <img src={illuMobiliser} alt="" class="mb-s16 w-full" />
        <h3 class="text-france-blue">Suivez vos demandes</h3>
        <p class="text-f16">
          <strong>Gardez une trace écrite de vos demandes</strong> et visualisez la
          réponse de la structure partenaire. Le tableau de suivi est maintenant intégré
          directement à la Plateforme de l’inclusion.
        </p>
        <a
          href={`${INCLUSION_PLATFORM_URL}/insertion/orientations/?mtm_campaign=DORA&mtm_kwd=homesuivi`}
          target="_blank"
          rel="noopener"
          class="text-f14 text-magenta-cta font-bold"
        >
          Suivez vos demandes envoyées<ExternalLinkIcon />
        </a>
      </div>
    {:else if selectedTabId === "porteurs"}
      <div class="md:basis-1/3">
        <img src={illuMobiliser} alt="" class="mb-s16 w-full" />
        <h3 class="text-france-blue">Suivez vos demandes reçues</h3>
        <p class="text-f16">
          <strong>Gardez une trace écrite de vos demandes reçues.</strong>
          Téléchargez la liste des orientations reçues par votre structure. Vous pourrez
          ainsi consulter et trier ces orientations. Fichier proposé au format .xls
        </p>
      </div>
      <div class="md:basis-1/3">
        <img src={illuRecenser} alt="" class="mb-s16 w-full" />
        <h3 class="text-france-blue">
          Donnez de la visibilité à votre offre de services
        </h3>
        <p class="text-f16">
          Avec plus de <strong>68 000 visiteurs</strong> uniques par mois et
          <strong>180 000 services actifs</strong>, DORA est l’annuaire de
          l’insertion de référence.
        </p>
      </div>
      <div class="md:basis-1/3">
        <img src={illuAccompagner} alt="" class="mb-s16 w-full" />
        <h3 class="text-france-blue">
          Centralisez les mises à jour de services
        </h3>
        <p class="text-f16">
          Saisissez ou importez vos services et mettez-les à jour, en un seul
          endroit ! DORA se charge de présenter vos données là où elles sont
          utiles, en <strong
            >les diffusant automatiquement sur plusieurs sites.</strong
          >
        </p>
      </div>
    {:else if selectedTabId === "particuliers"}
      <div class="md:basis-1/3">
        <img src={illuRecenser} alt="" class="mb-s16 w-full" />
        <h3 class="text-france-blue">Trouvez des services adaptés</h3>
        <p class="text-f16">
          DORA vous permet d’<strong
            >identifier les services d’insertion les plus adaptés</strong
          >
          à vos besoins.
        </p>
      </div>
      <div class="md:basis-1/3">
        <img src={illuAccompagner} alt="" class="mb-s16 w-full" />
        <h3 class="text-france-blue">Contactez les structures</h3>
        <p class="text-f16">
          Prenez contact avec les structures selon leurs préférences :
          téléphone, email, présentation à l’accueil, site du service…
        </p>
      </div>
    {/if}
  </div>

  <div
    class="gap-s16 bg-blue-light p-s16 md:px-s24 flex flex-col items-center justify-between rounded-2xl md:flex-row"
  >
    <p class="m-s0 p-s0 gap-s8 flex items-center font-bold">
      <PlayCircleFillMedia
        class="text-magenta-cta flex-none fill-current"
        aria-hidden="true"
      />
      Rejoignez-nous lors d'un webinaire pour explorer les possibilités offertes par
      DORA.
    </p>

    <LinkButton
      to={`${URL_HELP_SITE}article/participer-a-un-webinaire-dora-h3n747/`}
      otherTab
      nofollow
      small
      label="Je m’inscris"
    ></LinkButton>
  </div>
</CenteredGrid>

<CenteredGrid>
  <div>
    <p class="text-f12 text-center">
      Plus de 23 000 structures ont déjà commencé à référencer leurs services
      sur DORA
    </p>

    <ul class="mt-s24 flex w-full flex-wrap justify-center grayscale">
      <PartnerList partnersToShow={data.partnersToShow} imgHeight="small" />
    </ul>

    <div class="mt-s10 text-center">
      <a
        href="/nos-partenaires"
        class="text-f18 text-magenta-cta text-center underline"
      >
        Découvrez tous nos partenaires
      </a>
    </div>
  </div>

  <div
    class="mt-s64 gap-s24 bg-gray-bg p-s24 flex flex-col rounded-lg md:flex-row"
  >
    <div class="w-1/3 self-center text-center">
      <a href="https://data.inclusion.gouv.fr/">
        <img
          src={logoDataInclusion}
          alt="Data inclusion - Contributeur officiel"
          class="inline"
        />
      </a>
    </div>
    <div class="md:w-2/3">
      <h2 class="text-f17 text-gray-dark leading-24">Dites-le-nous une fois</h2>
      <p class="text-f16">
        Nous sommes engagés dans une démarche d’<span lang="en">Open Data</span>
        et rendons disponibles nos données à travers un référentiel commun — partagé
        par toutes les plateformes et sites web partenaires. Grâce à cette dynamique
        collective, vous référencez votre offre une seule fois tout en la rendant
        disponible partout.
      </p>
    </div>
  </div>
</CenteredGrid>

<MonRecapPopup />
