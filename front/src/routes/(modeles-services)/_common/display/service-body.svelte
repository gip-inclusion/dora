<script lang="ts">
  import { browser } from "$app/environment";
  import { page } from "$app/stores";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import OrientationVideo from "$lib/components/specialized/orientation-video.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { token, userInfo } from "$lib/utils/auth";
  import { trackMobilisation } from "$lib/utils/stats";

  import PreventFakeOrientationModal from "./modals/prevent-fake-orientation-modal.svelte";

  import ServiceBeneficiaries from "./service-beneficiaries.svelte";
  import ServiceMobilisation from "./service-mobilisation.svelte";
  import ServiceMobilize from "./service-mobilize.svelte";
  import SmallServiceShare from "./small-service-share.svelte";
  import ServicePresentation from "./service-presentation.svelte";
  import ServiceIndividual from "./service-individual.svelte";

  export let service: Service | Model;
  export let servicesOptions: ServicesOptions;

  export let isModel = false;
  export let isDI = false;

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
  <div class="mb-s48 gap-x-s48 flex flex-col justify-between md:flex-row">
    <div class="flex-auto basis-2/3">
      <div>
        <ServicePresentation {service} {servicesOptions} {isDI} />
      </div>
      <div class="main-content">
        <div>
          <hr class="my-s24" />
          <ServiceBeneficiaries {service} />
        </div>
        <hr class="my-s24" />
        <div class="mobilize">
          <ServiceMobilize
            on:trackMobilisation={handleTrackMobilisationEvent}
            {service}
            {orientationFormUrl}
            {handleOrientationFormClickEvent}
          />
        </div>
      </div>
    </div>

    {#if browser}
      <div class="gap-y-s24 flex flex-none flex-col md:w-[320px] lg:w-[375px]">
        {#if !isModel}
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

            {#if !isModel}
              <div class="mt-s24 gap-y-s24 flex flex-col">
                <SmallServiceShare {service} {isDI} />
              </div>
            {/if}
          </div>
        {/if}
      </div>
    {/if}
  </div>
</CenteredGrid>

<PreventFakeOrientationModal
  bind:isOpen={isPreventFakeOrientationModalOpen}
  on:showVideo={handleShowVideoModal}
  on:trackMobilisation={handleTrackMobilisationEvent}
  {orientationFormUrl}
/>
<OrientationVideo bind:isVideoModalOpen />
