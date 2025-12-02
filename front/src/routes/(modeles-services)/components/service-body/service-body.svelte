<script lang="ts">
  import { page } from "$app/stores";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import OrientationVideo from "$lib/components/specialized/orientation-video.svelte";
  import { DI_DORA_UNIFIED_SEARCH_ENABLED } from "$lib/env";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getToken, userInfo } from "$lib/utils/auth";
  import { isServiceRecentlyPublished } from "$lib/utils/service";
  import { trackMobilisation } from "$lib/utils/stats";

  import PreventFakeOrientationModal from "./prevent-fake-orientation-modal.svelte";
  import ServiceMobilisation from "./service-mobilisation.svelte";
  import ServicePresentation from "./service-presentation/service-presentation.svelte";
  import ServiceIndividual from "./service-individual.svelte";

  interface Props {
    service: Service | Model;
    servicesOptions: ServicesOptions;
    onFeedbackButtonClick?: () => void;
  }

  let { service, servicesOptions, onFeedbackButtonClick }: Props = $props();

  let isDI = $derived("source" in service);

  let searchIdStr = $derived($page.url.searchParams.get("searchId"));
  let searchIdNumber = $derived(
    searchIdStr ? parseInt(searchIdStr) : undefined
  );
  let searchFragment = $derived(searchIdStr ? `?searchId=${searchIdStr}` : "");
  let orientationFormUrl = $derived(
    `/services/${isDI ? "di--" : ""}${service.slug}/orienter${searchFragment}`
  );

  let isServiceFromOwnStructure = $derived(
    $userInfo
      ? [...$userInfo.structures, ...$userInfo.pendingStructures].some(
          (structure) => structure.slug === service.structure
        )
      : false
  );

  let showServiceWillBeVisibleSoonNotice = $derived(
    DI_DORA_UNIFIED_SEARCH_ENABLED &&
      !service.isModel &&
      service.status === "PUBLISHED" &&
      service.canWrite &&
      isServiceRecentlyPublished(service)
  );

  // Utilisé pour prévenir le tracking multiple
  let mobilisationTracked = $state(false);

  let isPreventFakeOrientationModalOpen = $state(false);
  let isVideoModalOpen = $state(false);

  function handleShowVideoModal() {
    isPreventFakeOrientationModalOpen = false;
    isVideoModalOpen = true;
  }

  function handleTrackMobilisation(externalUrl?: string) {
    if (!mobilisationTracked) {
      trackMobilisation(service, $page.url, isDI, searchIdNumber, externalUrl);
      mobilisationTracked = true;
    }
  }

  function handleOrientationFormClickEvent(event) {
    if (isServiceFromOwnStructure) {
      event.preventDefault();
      isPreventFakeOrientationModalOpen = true;
    } else if (getToken()) {
      handleTrackMobilisation();
    }
  }
</script>

<CenteredGrid>
  <div class="md:gap-s48 mb-s32 flex flex-col md:flex-row">
    <div class="gap-s32 flex basis-2/3 flex-col">
      {#if showServiceWillBeVisibleSoonNotice}
        <Notice
          title="Votre service est publié et sera bientôt visible partout"
          type="warning"
        >
          <p class="text-f14 text-gray-dark mb-s0">
            Il apparaitra dans les résultats de recherche et sur les plateformes
            partenaires via le référentiel commun data·inclusion dans un délai
            d’une heure.
          </p>
        </Notice>
      {/if}
      <div class="text-f18 leading-s32 text-gray-text">
        <p>
          {service.shortDesc || ""}
        </p>
      </div>
    </div>
    <div class="basis-1/3"></div>
  </div>

  <div class="gap-s48 grid grid-cols-1 md:grid-cols-3">
    <div class="md:col-span-2">
      <ServicePresentation
        {service}
        {servicesOptions}
        {onFeedbackButtonClick}
        onTrackMobilisation={handleTrackMobilisation}
      />
    </div>

    <div class="gap-y-s24 flex flex-col">
      {#if !service.isModel}
        <div class="top-s32 sticky">
          <div
            class="border-gray-02 bg-france-blue p-s24 px-s32 block rounded-3xl border text-white print:hidden"
          >
            <ServiceMobilisation
              onTrackMobilisation={handleTrackMobilisation}
              {service}
              {isDI}
              {orientationFormUrl}
              {handleOrientationFormClickEvent}
            />
          </div>

          {#if !$userInfo && service.source === "mes-aides" && service.lienSource}
            <div class="mb-s8 mt-s16">
              <ServiceIndividual url={service.lienSource} />
            </div>
          {/if}
        </div>
      {/if}
    </div>
  </div>
</CenteredGrid>

<PreventFakeOrientationModal
  bind:isOpen={isPreventFakeOrientationModalOpen}
  onShowVideo={handleShowVideoModal}
  onTrackMobilisation={handleTrackMobilisation}
  {orientationFormUrl}
/>
<OrientationVideo bind:isVideoModalOpen />
