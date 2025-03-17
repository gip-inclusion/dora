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
  import MonRecapPopup from "$lib/components/specialized/mon-recap-popup.svelte";

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
</script>

{#if data.service}
  <CenteredGrid bgColor="bg-blue-light">
    <ServiceHeader service={data.service} />
  </CenteredGrid>

  <CenteredGrid roundedColor="bg-blue-light">
    <ServiceToolbar
      service={data.service}
      servicesOptions={data.servicesOptions}
      onRefresh={handleRefresh}
    />
  </CenteredGrid>

  <ServiceBody service={data.service} servicesOptions={data.servicesOptions} />

  {#if browser && data.service.canWrite && serviceWasJustPublished && !data.service.hasAlreadyBeenUnpublished}
    <TallyPopup
      formId={TallyFormId.SERVICE_CREATION_FORM_ID}
      timeoutSeconds={3}
    />
  {/if}

  <MonRecapPopup />
{/if}
