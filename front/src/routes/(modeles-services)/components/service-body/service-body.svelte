<script lang="ts">
  import { page } from "$app/stores";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import OrientationVideo from "$lib/components/specialized/orientation-video.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { token, userInfo } from "$lib/utils/auth";
  import { trackMobilisation } from "$lib/utils/stats";

  import PreventFakeOrientationModal from "./prevent-fake-orientation-modal.svelte";
  import ServiceMobilisation from "./service-mobilisation.svelte";
  import ServicePresentation from "./service-presentation/service-presentation.svelte";
  import ServiceIndividual from "./service-individual.svelte";
  import ServiceDescription from "./service-description.svelte";

  export let service: Service | Model;
  export let servicesOptions: ServicesOptions;

  $: isDI = "source" in service;

  $: searchIdStr = $page.url.searchParams.get("searchId");
  $: searchIdNumber = searchIdStr ? parseInt(searchIdStr) : undefined;
  $: searchFragment = searchIdStr ? `?searchId=${searchIdStr}` : "";
  $: orientationFormUrl = `/services/${isDI ? "di--" : ""}${service.slug}/orienter${searchFragment}`;

  $: isServiceFromOwnStructure = $userInfo
    ? [...$userInfo.structures, ...$userInfo.pendingStructures].some(
        (structure) => structure.slug === service.structure
      )
    : false;

  // Utilisé pour prévenir le tracking multiple
  let mobilisationTracked = false;

  let isPreventFakeOrientationModalOpen = false;
  let isVideoModalOpen = false;

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
  function handleTrackMobilisationEvent(
    event: CustomEvent<{ externalUrl?: string }>
  ) {
    handleTrackMobilisation(event.detail.externalUrl);
  }

  function handleOrientationFormClickEvent(event) {
    if (isServiceFromOwnStructure) {
      event.preventDefault();
      isPreventFakeOrientationModalOpen = true;
    } else if ($token) {
      handleTrackMobilisation();
    }
  }
</script>

<CenteredGrid>
  <div class="md:gap-s48 mb-s32 flex flex-col md:flex-row">
    <div class="basis-2/3">
      <div class="text-f16 leading-s32 text-gray-text">
        <p>
          {service.shortDesc || ""}
        </p>
        {#if service.fullDesc}
          <ServiceDescription {service} />
        {/if}
      </div>
    </div>
    <div class="basis-1/3" />
  </div>

  <div class="gap-s48 flex flex-col md:flex-row">
    <div class="basis-2/3">
      <ServicePresentation {service} {servicesOptions} {isDI} />
    </div>

    <div class="gap-y-s24 flex basis-1/3 flex-col">
      {#if !service.isModel}
        <div class="top-s32 sticky">
          <div
            class="border-gray-02 bg-france-blue p-s24 px-s32 block rounded-3xl border text-white print:hidden"
          >
            <ServiceMobilisation
              on:trackMobilisation={handleTrackMobilisationEvent}
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
  on:showVideo={handleShowVideoModal}
  on:trackMobilisation={handleTrackMobilisationEvent}
  {orientationFormUrl}
/>
<OrientationVideo bind:isVideoModalOpen />
