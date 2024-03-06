<script lang="ts">
  import { browser } from "$app/environment";
  import { page } from "$app/stores";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import ServiceHeader from "./service-header.svelte";
  import ServiceToolbar from "./service-toolbar.svelte";
  import TallyPopup from "$lib/components/specialized/tally-popup.svelte";
  import ServiceBody from "../../_common/display/service-body.svelte";
  import { getService } from "$lib/requests/services";
  import { TallyFormId } from "$lib/consts";

  import { trackService } from "$lib/utils/stats";
  import { onMount } from "svelte";
  import type { PageData } from "./$types";
  import type { Service } from "$lib/types";

  export let data: PageData;

  onMount(() => {
    const searchId = $page.url.searchParams.get("searchId");
    trackService(data.service, $page.url, searchId, data.isDI);
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

  $: structureHasPublishedServices = data.structure?.services.filter(
    (service) => service.status === "PUBLISHED"
  ).length;
</script>

{#if data.service}
  <CenteredGrid bgColor="bg-france-blue print:bg-white">
    <ServiceHeader service={data.service} isDI={data.isDI} />
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
    isDI={data.isDI}
  />

  {#if browser}
    {#if data.service.canWrite}
      {#if serviceWasJustPublished && !data.service.hasAlreadyBeenUnpublished}
        <TallyPopup
          formId={TallyFormId.SERVICE_CREATION_FORM_ID}
          timeoutSeconds={3}
        />
      {:else if structureHasPublishedServices}
        <TallyPopup
          formId={TallyFormId.NPS_FORM_ID}
          keySuffix="offreur"
          timeoutSeconds={30}
          hiddenFields={{ user: "offreur" }}
        />
      {/if}
    {:else}
      <TallyPopup
        formId={TallyFormId.NPS_FORM_ID}
        keySuffix="chercheur"
        timeoutSeconds={45}
        hiddenFields={{ user: "chercheur" }}
      />
    {/if}
  {/if}
{/if}
