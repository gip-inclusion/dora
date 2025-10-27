<script lang="ts">
  import VideoFillMedia from "svelte-remix/VideoFillMedia.svelte";

  import illuAccompagner from "$lib/assets/illustrations/illu-accompagner.svg";
  import illuMobiliser from "$lib/assets/illustrations/illu-mobiliser.svg";
  import illuRecenser from "$lib/assets/illustrations/illu-recenser.svg";
  import logoDataInclusion from "$lib/assets/logos/logo-data-inclusion.svg";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import InviteStructureLink from "$lib/components/specialized/invite-structure-link.svelte";
  import PartnerList from "$lib/components/specialized/partner-list.svelte";
  import SearchForm from "$lib/components/specialized/service-search.svelte";
  import OrientationVideo from "$lib/components/specialized/orientation-video.svelte";
  import { GOOGLE_CSE_ID } from "$lib/env";
  import { refreshUserInfo } from "$lib/utils/auth";
  import { userInfo } from "$lib/utils/auth";
  import { userPreferences } from "$lib/utils/preferences";
  import ServicesToUpdateNotice from "./structures/[slug]/services/services-to-update-notice.svelte";
  import MonRecapPopup from "$lib/components/specialized/mon-recap-popup.svelte";
  import { getCurrentlySelectedStructure } from "$lib/utils/current-structure";

  import type { PageData } from "./$types";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  let isVideoModalOpen = $state(false);

  let lastVisitedStructure = $derived(
    getCurrentlySelectedStructure($userInfo, $userPreferences)
  );
</script>

<OrientationVideo bind:isVideoModalOpen></OrientationVideo>

<CenteredGrid bgColor="bg-magenta-10 mb-s32">
  <h1 class="mb-s16 text-france-blue m-auto text-center text-balance">
    Orientez vos bénéficiaires vers des solutions adaptées à leurs besoins
  </h1>
  <div class="mb-s32">
    <p class="text-f16 text-gray-text m-auto text-center text-balance">
      DORA est un outil d’aide à la prescription qui vous accompagne dans la
      levée des freins périphériques.
    </p>
  </div>

  <SearchForm
    servicesOptions={data.servicesOptions}
    cityCode={data.cityCode}
    cityLabel={data.cityLabel}
    label={data.cityLabel}
    initialSearch
  />

  {#if GOOGLE_CSE_ID}
    <div class="mt-s32 mb-s32 flex items-center justify-center">
      <div class="mr-s16">ou</div>
      <LinkButton
        label="Faire une recherche par mots-clés"
        to={`/recherche-textuelle`}
      />
    </div>
  {/if}
</CenteredGrid>

<CenteredGrid>
  {#if lastVisitedStructure?.canEditInformations}
    <div class="mb-s44">
      <ServicesToUpdateNotice
        structureSlug={lastVisitedStructure.slug}
        servicesToUpdate={lastVisitedStructure.servicesToUpdate}
        onRefresh={refreshUserInfo}
      />
    </div>
  {/if}
  <h2 class="mb-s32 text-france-blue text-center">
    Comment DORA peut vous aider
  </h2>
  <div class="mb-s24 gap-s24 flex flex-col md:flex-row">
    <div class="md:flex-1">
      <img src={illuRecenser} alt="" class="mb-s16 w-full" />
      <div class="tag bg-[#003895]">Recherche simplifiée</div>
      <h3>Identifier des services</h3>
      <p class="text-f16">
        DORA vous permet d’<strong
          >identifier les services d’insertion les plus adaptés</strong
        >
        aux besoins spécifiques de vos bénéficiaires.
      </p>
    </div>
    <div class="md:flex-1">
      <img src={illuAccompagner} alt="" class="mb-s16 w-full" />
      <div class="tag bg-info">Nouvelle fonctionnalité !</div>
      <h3>Orienter vos bénéficiaires</h3>
      <p class="text-f16">
        Le formulaire DORA <strong
          >facilite l’orientation de vos bénéficiaires</strong
        >
        vers la solution identifiée, le tout en
        <strong>moins de 5 minutes</strong>.

        <Button
          label="Voir la vidéo de démonstration"
          onclick={() => (isVideoModalOpen = true)}
          noBackground
          noPadding
        />
      </p>
    </div>
    <div class="md:flex-1">
      <img src={illuMobiliser} alt="" class="mb-s16 w-full" />
      <div class="tag bg-blue-information text-gray-text!">Très bientôt !</div>
      <h3>Suivre vos demandes</h3>
      <p class="text-f16">
        La structure partenaire répondra rapidement à votre demande. Vous
        pourrez <strong>suivre l’ensemble de vos demandes d’orientation</strong>
        depuis votre espace DORA.
      </p>
    </div>
  </div>

  <div
    class="border-gray-01 p-s16 md:gap-s32 flex flex-col items-center justify-between rounded-2xl border text-center md:flex-row md:items-baseline"
  >
    <p class="m-s0 p-s0">
      <span
        class="h-s24 w-s24 text-france-blue inline-block flex-none fill-current align-bottom"
      >
        <VideoFillMedia />
      </span>
      Rejoignez-nous lors d'un webinaire pour explorer les possibilités offertes
      par DORA.
    </p>

    <LinkButton
      to="https://aide.dora.inclusion.beta.gouv.fr/fr/article/participer-a-un-webinaire-dora-h3n747/"
      otherTab
      nofollow
      noBackground
      label="En savoir plus"
    ></LinkButton>
  </div>
</CenteredGrid>

<CenteredGrid>
  <div class="gap-s24 flex flex-col">
    <div class="text-center">
      <h2 class="text-france-blue">
        Donnez de la visibilité à votre offre de services
      </h2>
      <p class="mb-s0 m-auto w-3/4">
        Saisissez ou importez vos services et mettez-les à jour, en un seul
        endroit ! DORA se charge de présenter vos données là où elles sont
        utiles, en les diffusant automatiquement sur plusieurs sites.
      </p>
    </div>
    <div class="gap-s16 flex flex-wrap justify-center">
      <LinkButton label="Référencer vos services" to={`/services/creer`} />
      <InviteStructureLink />
    </div>

    <div class="mt-s16">
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

<style lang="postcss">
  @reference "../app.css";

  h3 {
    @apply text-france-blue;
  }

  .tag {
    @apply px-s8 py-s2 text-f12 w-fit rounded-sm font-bold text-white uppercase;
  }
</style>
