<script lang="ts">
  import { onMount, setContext } from "svelte";

  import { browser } from "$app/environment";
  import { page } from "$app/stores";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import MonRecapPopup from "$lib/components/specialized/mon-recap-popup.svelte";
  import TallyPopup from "$lib/components/specialized/tally-popup.svelte";
  import { TallyFormId } from "$lib/consts";
  import { getService } from "$lib/requests/services";
  import type { Service } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { isMemberOrPotentialMemberOfStructure } from "$lib/utils/current-structure";
  import { trackService } from "$lib/utils/stats";

  import ServiceBody from "../../components/service-body/service-body.svelte";
  import ServiceFeedbackModal from "./service-feedback-modal.svelte";
  import ServiceHeader from "./service-header.svelte";
  import ServiceToolbar from "./service-toolbar.svelte";
  import type { PageData } from "./$types";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  let reactiveData = $state(data);

  let isServiceFeedbackModalOpen = $state(false);

  let showFeedbackModal = $derived(
    browser &&
      reactiveData.service &&
      !isMemberOrPotentialMemberOfStructure(
        $userInfo,
        reactiveData.service.structure
      )
  );

  $effect(() => {
    setContext("showFeedbackModal", showFeedbackModal);
  });

  onMount(() => {
    const searchId = $page.url.searchParams.get("searchId");
    trackService(reactiveData.service, $page.url, searchId, reactiveData.isDI);
  });

  async function handleRefresh() {
    if (reactiveData.service) {
      reactiveData.service = await getService(reactiveData.service.slug);
    }
  }

  function getMinutesSincePublication(service: Service) {
    return (
      (new Date().getTime() - new Date(service.publicationDate).getTime()) /
      60000
    );
  }

  const serviceWasJustPublished =
    reactiveData.service &&
    reactiveData.service.publicationDate &&
    reactiveData.service.status === "PUBLISHED" &&
    getMinutesSincePublication(reactiveData.service) < 1;
</script>

{#if reactiveData.service}
  <CenteredGrid bgColor="bg-blue-light">
    <ServiceHeader service={reactiveData.service} />
  </CenteredGrid>

  <CenteredGrid roundedColor="bg-blue-light" noPadding extraClass="mb-s8">
    <ServiceToolbar
      service={reactiveData.service}
      servicesOptions={reactiveData.servicesOptions}
      onRefresh={handleRefresh}
      onFeedbackButtonClick={() => (isServiceFeedbackModalOpen = true)}
    />
  </CenteredGrid>

  <ServiceBody
    service={reactiveData.service}
    servicesOptions={reactiveData.servicesOptions}
    onFeedbackButtonClick={() => (isServiceFeedbackModalOpen = true)}
  />

  {#if showFeedbackModal}
    <ServiceFeedbackModal
      bind:isOpen={isServiceFeedbackModalOpen}
      service={reactiveData.service}
    />
  {/if}

  {#if browser && reactiveData.service.canWrite && serviceWasJustPublished && !reactiveData.service.hasAlreadyBeenUnpublished}
    <TallyPopup
      formId={TallyFormId.SERVICE_CREATION_FORM_ID}
      timeoutSeconds={3}
    />
  {/if}

  <MonRecapPopup />
{/if}
