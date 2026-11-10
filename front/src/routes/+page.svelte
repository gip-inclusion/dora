<script lang="ts">
  import PlayCircleFillMedia from "svelte-remix/PlayCircleFillMedia.svelte";

  import logoDataInclusion from "$lib/assets/logos/logo-data-inclusion.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Tabs from "$lib/components/display/tabs.svelte";
  import PartnerList from "$lib/components/specialized/partner-list.svelte";
  import SearchForm from "$lib/components/specialized/service-search.svelte";
  import { refreshUserInfo, userInfo } from "$lib/utils/auth";
  import { userPreferences } from "$lib/utils/preferences";
  import HomeTabPanel, {
    homeTabs,
    type HomeTabId,
  } from "./_index/home-tab-panel.svelte";
  import ServicesToUpdateNotice from "./structures/[slug]/services/services-to-update-notice.svelte";
  import MonRecapPopup from "$lib/components/specialized/mon-recap-popup.svelte";
  import { getCurrentlySelectedStructure } from "$lib/utils/current-structure";

  import type { PageData } from "./$types";
  import { URL_HELP_SITE } from "$lib/consts";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  let selectedTabId = $state<HomeTabId>("accompagnement");

  let lastVisitedStructure = $derived(
    getCurrentlySelectedStructure($userInfo, $userPreferences)
  );
</script>

<CenteredGrid extraClass="pt-s32" bgColor="bg-magenta-10" noPadding>
  <h1 class="mb-s32 text-france-blue m-auto text-center text-balance">
    Trouvez le service adapté<br />pour lever les freins à l’insertion
  </h1>

  <SearchForm
    servicesOptions={data.servicesOptions}
    cityCode={data.cityCode}
    cityLabel={data.cityLabel}
    label={data.label}
    lon={data.lon}
    lat={data.lat}
    initialSearch
  />
  <div class="mt-s32 flex items-center justify-center">
    <div class="mr-s16">ou</div>
    <LinkButton
      label="Faire une recherche par mots-clés"
      to={`/recherche-mots-cles`}
    />
  </div>

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
  <HomeTabPanel tabId={selectedTabId} />

  <div
    class="mt-s32 gap-s16 bg-blue-light p-s16 md:px-s24 flex flex-col items-center justify-between rounded-2xl md:flex-row"
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
