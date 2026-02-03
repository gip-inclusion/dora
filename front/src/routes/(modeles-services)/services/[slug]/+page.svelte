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

  export type ShowFeedbackModalContext = () => boolean;

  let { data }: Props = $props();

  let reactiveData = $state(data);

  let { service, servicesOptions, isDI } = $derived(reactiveData);

  let isServiceFeedbackModalOpen = $state(false);

  let showFeedbackModal = $derived(
    Boolean(
      browser &&
      service &&
      !isMemberOrPotentialMemberOfStructure($userInfo, service.structure)
    )
  );

  setContext<ShowFeedbackModalContext>(
    "showFeedbackModal",
    () => showFeedbackModal
  );

  onMount(() => {
    const searchId = $page.url.searchParams.get("searchId");
    trackService(service, $page.url, searchId, isDI);
  });

  async function handleRefresh() {
    if (service) {
      service = await getService(service.slug);
    }
  }

  function getMinutesSincePublication(serv: Service) {
    return (
      (new Date().getTime() - new Date(serv.publicationDate).getTime()) / 60000
    );
  }

  const serviceWasJustPublished = $derived(
    service &&
      service.publicationDate &&
      service.status === "PUBLISHED" &&
      getMinutesSincePublication(service) < 1
  );
</script>

{#if service && servicesOptions}
  <CenteredGrid bgColor="bg-blue-light">
    <ServiceHeader {service} />
  </CenteredGrid>

  <CenteredGrid roundedColor="bg-blue-light" noPadding extraClass="mb-s8">
    <ServiceToolbar
      {service}
      {servicesOptions}
      onRefresh={handleRefresh}
      onFeedbackButtonClick={() => (isServiceFeedbackModalOpen = true)}
    />
  </CenteredGrid>

  <ServiceBody
    {service}
    {servicesOptions}
    onFeedbackButtonClick={() => (isServiceFeedbackModalOpen = true)}
  />

  {#if showFeedbackModal}
    <ServiceFeedbackModal bind:isOpen={isServiceFeedbackModalOpen} {service} />
  {/if}

  {#if browser && service.canWrite && serviceWasJustPublished && !service.hasAlreadyBeenUnpublished}
    <TallyPopup
      formId={TallyFormId.SERVICE_CREATION_FORM_ID}
      timeoutSeconds={3}
    />
  {/if}

  <MonRecapPopup />
{/if}
