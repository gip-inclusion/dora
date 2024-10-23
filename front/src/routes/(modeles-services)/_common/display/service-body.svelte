<script lang="ts">
  import { browser } from "$app/environment";
  import { page } from "$app/stores";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { trackMobilisation } from "$lib/utils/stats";

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

  // Utilisé pour prévenir le tracking multiple
  let mobilisationTracked = false;

  function handleTrackMobilisation(
    event: CustomEvent<{ externalUrl?: string }>
  ) {
    if (!mobilisationTracked) {
      const searchIdStr = $page.url.searchParams.get("searchId");
      const searchId = searchIdStr ? parseInt(searchIdStr) : undefined;
      trackMobilisation(
        service,
        $page.url,
        isDI,
        searchId,
        event.detail.externalUrl
      );
      mobilisationTracked = true;
    }
  }
</script>

<CenteredGrid>
  <div class="mb-s48 flex flex-col justify-between gap-x-s48 md:flex-row">
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
            on:trackMobilisation={handleTrackMobilisation}
            {service}
            {isDI}
          />
        </div>
      </div>
    </div>

    {#if browser}
      <div class="flex flex-none flex-col gap-y-s24 md:w-[320px] lg:w-[375px]">
        {#if !isModel}
          <div class="sticky top-s32">
            <div
              class="block rounded-lg border border-gray-02 bg-france-blue p-s24 px-s32 text-white print:hidden"
            >
              <ServiceMobilisation
                on:trackMobilisation={handleTrackMobilisation}
                {service}
                {isDI}
              />
            </div>

            {#if !$userInfo && service.source === "mes-aides" && service.lienSource}
              <div class="mb-s8 mt-s16">
                <ServiceIndividual url={service.lienSource} />
              </div>
            {/if}

            {#if !isModel}
              <div class="mt-s24 flex flex-col gap-y-s24">
                <SmallServiceShare {service} {isDI} />
              </div>
            {/if}
          </div>
        {/if}
      </div>
    {/if}
  </div>
</CenteredGrid>
