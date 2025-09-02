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

  let { data = $bindable() }: Props = $props();

  let isServiceFeedbackModalOpen = $state(false);

  let showFeedbackModal = $derived(
    Boolean(
      browser &&
        data.service &&
        !isMemberOrPotentialMemberOfStructure($userInfo, data.service.structure)
    )
  );

  setContext<ShowFeedbackModalContext>(
    "showFeedbackModal",
    () => showFeedbackModal
  );

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

  <CenteredGrid roundedColor="bg-blue-light" noPadding extraClass="mb-s8">
    <ServiceToolbar
      service={data.service}
      servicesOptions={data.servicesOptions}
      onRefresh={handleRefresh}
      onFeedbackButtonClick={() => (isServiceFeedbackModalOpen = true)}
    />
  </CenteredGrid>

  <ServiceBody
    service={data.service}
    servicesOptions={data.servicesOptions}
    onFeedbackButtonClick={() => (isServiceFeedbackModalOpen = true)}
  />

  {#if showFeedbackModal}
    <ServiceFeedbackModal
      bind:isOpen={isServiceFeedbackModalOpen}
      service={data.service}
    />
  {/if}

  {#if browser && data.service.canWrite && serviceWasJustPublished && !data.service.hasAlreadyBeenUnpublished}
    <TallyPopup
      formId={TallyFormId.SERVICE_CREATION_FORM_ID}
      timeoutSeconds={3}
    />
  {/if}

  <MonRecapPopup />
{/if}
