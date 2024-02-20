<script lang="ts">
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
  import Modal from "$lib/components/hoc/modal.svelte";

  import type { PageData } from "./$types";
  import { browser } from "$app/environment";
  import { videoIcon } from "$lib/icons";

  export let data: PageData;

  let isVideoModalOpen = false;
</script>

{#if browser}
  <Modal
    bind:isOpen={isVideoModalOpen}
    title="Le formulaire d’orientation"
    width="medium"
  >
    <div style="position: relative; padding-top: 50%;">
      <iframe
        title="DORA - Orienter un bénéficiaire"
        width="100%"
        height="100%"
        src="https://tube.numerique.gouv.fr/videos/embed/c620b3c6-d9c8-46aa-8ab6-42b14b3f45a0?subtitle=fr&amp;warningTitle=0&amp;peertubeLink=0&amp;p2p=0"
        frameborder="0"
        allowfullscreen
        sandbox="allow-same-origin allow-scripts allow-popups"
        style="position: absolute; inset: 0px;"
      ></iframe>
    </div>
  </Modal>
{/if}

<CenteredGrid bgColor="bg-magenta-10 mb-s32">
  <h1 class="m-auto mb-s16 text-balance text-center text-france-blue">
    Orientez vos bénéficiaires vers des solutions adaptées à leurs besoins
  </h1>
  <div class="mb-s32">
    <p class="m-auto text-balance text-center text-f16 text-gray-text">
      DORA est un outil d’aide à la prescription qui vous accompagne dans la
      levée des freins périphériques.
    </p>
  </div>

  <SearchForm
    servicesOptions={data.servicesOptions}
    cityCode={data.cityCode}
    cityLabel={data.cityLabel}
    label={data.cityLabel}
  />
</CenteredGrid>

<CenteredGrid>
  <h2 class="mb-s32 text-center text-france-blue">
    Comment DORA peut vous aider
  </h2>
  <div class="mb-s24 flex flex-col gap-s24 md:flex-row">
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
          on:click={() => (isVideoModalOpen = true)}
          noBackground
          noPadding
        />
      </p>
    </div>
    <div class="md:flex-1">
      <img src={illuMobiliser} alt="" class="mb-s16 w-full" />
      <div class="tag bg-blue-information !text-gray-text">Très bientôt !</div>
      <h3>Suivre vos demandes</h3>
      <p class="text-f16">
        La structure partenaire répondra rapidement à votre demande. Vous
        pourrez <strong>suivre l’ensemble de vos demandes d’orientation</strong>
        depuis votre espace DORA.
      </p>
    </div>
  </div>

  <div
    class=" flex flex-col items-center justify-between rounded-ml border border-gray-01 p-s16 text-center md:flex-row md:items-baseline md:gap-s32"
  >
    <p class="m-s0 p-s0">
      <span
        class="inline-block h-s24 w-s24 flex-none fill-current align-bottom text-france-blue"
      >
        {@html videoIcon}
      </span>
      Rejoignez-nous lors d'un webinaire pour explorer les possibilités offertes
      par DORA.
    </p>

    <LinkButton
      to="https://app.livestorm.co/dora-1"
      otherTab
      nofollow
      noBackground
      label="Consulter le calendrier"
    ></LinkButton>
  </div>
</CenteredGrid>

<CenteredGrid>
  <div class="flex flex-col gap-s24">
    <div class="text-center">
      <h2 class="text-france-blue">
        Donnez de la visibilité à votre offre de services
      </h2>
      <p class="m-auto mb-s0 w-3/4">
        Saisissez ou importez vos services et mettez-les à jour, en un seul
        endroit ! DORA se charge de présenter vos données là où elles sont
        utiles, en les diffusant automatiquement sur plusieurs sites.
      </p>
    </div>
    <div class="flex flex-wrap justify-center gap-s16">
      <LinkButton label="Référencer vos service" to={`/services/creer`} />
      <InviteStructureLink />
    </div>

    <div class="mt-s16">
      <p class="text-center text-f12">
        Plus de 5 000 structures ont déjà commencé à référencer leurs services
        sur DORA
      </p>

      <ul class="mt-s24 flex w-full flex-wrap justify-center grayscale">
        <PartnerList partnersToShow={data.partnersToShow} imgHeight="small" />
      </ul>

      <div class="mt-s10 text-center">
        <a
          href="/nos-partenaires"
          class="text-center text-f18 text-magenta-cta underline"
        >
          Découvrez tous nos partenaires
        </a>
      </div>
    </div>
  </div>

  <div
    class="mt-s64 flex flex-col gap-s24 rounded-md bg-gray-bg p-s24 md:flex-row"
  >
    <div class="w-1/3 self-center text-center">
      <a href="https://www.data.inclusion.beta.gouv.fr/">
        <img
          src={logoDataInclusion}
          alt="Data inclusion - Contributeur officiel"
          class="inline"
        />
      </a>
    </div>
    <div class="md:w-2/3">
      <h2 class="text-f17 leading-24 text-gray-dark">Dites-le-nous une fois</h2>
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

<style lang="postcss">
  h3 {
    @apply text-france-blue;
  }

  .tag {
    @apply w-fit rounded px-s8 py-s2 text-f12 font-bold uppercase text-white;
  }
</style>
