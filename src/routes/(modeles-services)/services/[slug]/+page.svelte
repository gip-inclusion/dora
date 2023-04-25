<script lang="ts">
  import { browser } from "$app/environment";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import ServiceHeader from "./service-header.svelte";
  import ServiceToolbar from "./service-toolbar.svelte";
  import TallyNpsPopup from "$lib/components/specialized/tally-nps-popup.svelte";
  import ServiceBody from "../../_common/display/service-body.svelte";
  import { getService } from "$lib/requests/services";
  import { token } from "$lib/utils/auth";
  import { TallyFormId } from "$lib/utils/nps";
  import { trackService } from "$lib/utils/plausible";
  import { onMount } from "svelte";
  import type { PageData } from "./$types";
  import type { Service } from "$lib/types";

  export let data: PageData;

  onMount(() => {
    trackService(data.service);
  });

  async function handleRefresh() {
    if (data.service) {
      data.service = await getService(data.service.slug);
    }
  }

  function getMinutesSincePublication(service: Service) {
    return (
      (new Date().getTime() - new Date(service.publicationDate).getTime()) /
      60000
    );
  }

  const serviceWasJustPublished =
    data.service &&
    data.service.publicationDate &&
    data.service.status === "PUBLISHED" &&
    getMinutesSincePublication(data.service) < 1;

  $: showContact = data.service?.isContactInfoPublic || $token;
  $: structureHasPublishedServices = data.structure?.services.filter(
    (service) => service.status === "PUBLISHED"
  ).length;
</script>

{#if data.service}
  <CenteredGrid bgColor="bg-france-blue">
    <ServiceHeader service={data.service} />
  </CenteredGrid>

  <div>
    <ServiceToolbar
      service={data.service}
      servicesOptions={data.servicesOptions}
      onRefresh={handleRefresh}
    />
  </div>

  <ServiceBody
    service={data.service}
    servicesOptions={data.servicesOptions}
    {showContact}
  />

  {#if browser}
    {#if data.service.canWrite}
      {#if serviceWasJustPublished && !data.service.hasAlreadyBeenUnpublished}
        <TallyNpsPopup
          formId={TallyFormId.SERVICE_CREATION_FORM_ID}
          timeoutSeconds={3}
        />
      {:else if structureHasPublishedServices}
        <TallyNpsPopup
          formId={TallyFormId.NPS_FORM_ID}
          keySuffix="offreur"
          timeoutSeconds={30}
          hiddenFields={{ user: "offreur" }}
        />
      {/if}
    {:else}
      <TallyNpsPopup
        formId={TallyFormId.NPS_FORM_ID}
        keySuffix="chercheur"
        timeoutSeconds={45}
        hiddenFields={{ user: "chercheur" }}
      />
    {/if}
  {/if}
{/if}
