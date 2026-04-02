<script lang="ts">
  import { onMount, setContext } from "svelte";

  import { browser } from "$app/environment";
  import { beforeNavigate } from "$app/navigation";
  import { page } from "$app/stores";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import MonRecapPopup from "$lib/components/specialized/mon-recap-popup.svelte";
  import TallyPopup from "$lib/components/specialized/tally-popup.svelte";
  import {
    ORIENTATION_JWT_QUERY_PARAM,
    TallyFormId,
    TOAST_DURATION_MS,
  } from "$lib/consts";
  import { getService } from "$lib/requests/services";
  import type { Service } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { isMemberOrPotentialMemberOfStructure } from "$lib/utils/current-structure";
  import { setCurrentStructure } from "$lib/utils/preferences";
  import { trackService } from "$lib/utils/stats";

  import ServiceBody from "../../components/service-body/service-body.svelte";
  import ServiceFeedbackModal from "./service-feedback-modal.svelte";
  import ServiceHeader from "./service-header.svelte";
  import ServiceToolbar from "./service-toolbar.svelte";
  import type { PageData } from "./$types";
  import { toast } from "@zerodevx/svelte-toast";

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

  $effect(() => {
    const userStructureSlug = $page.url.searchParams.get("user_structure_slug");
    if (userStructureSlug && $userInfo) {
      const userStructure = [
        ...$userInfo.pendingStructures,
        ...$userInfo.structures,
      ].find((struct) => struct.slug === userStructureSlug);

      if (userStructure && setCurrentStructure(userStructureSlug)) {
        toast.push({
          msg: `Votre structure active a été automatiquement modifiée : vous utilisez désormais ${userStructure.name}.<br/><br/>Attention : si d'autres onglets DORA sont ouverts dans votre navigateur, votre activité dans ces onglets sera également associée à la structure ${userStructure.name}.`,
          theme: {
            "--toastWidth": "50%",
          },
          duration: TOAST_DURATION_MS,
        });
      }
    }
  });

  beforeNavigate(({ from, to }) => {
    if (!from || !to) {
      return;
    }

    const hasEmploisOrientation = from.url.searchParams.has(
      ORIENTATION_JWT_QUERY_PARAM
    );
    if (!hasEmploisOrientation) {
      return;
    }

    const isGoingToOrienter = to.url.pathname.match(
      /^\/services\/[^/]+\/orienter/
    );
    if (!isGoingToOrienter) {
      const cleanUrl = new URL(from.url);
      cleanUrl.searchParams.delete(ORIENTATION_JWT_QUERY_PARAM);
      cleanUrl.searchParams.delete("user_structure_slug");
      history.replaceState({}, "", cleanUrl);
    }
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

<style>
  :global(._toastItem) {
    top: 5.1rem !important;
    left: 50% !important;
    right: auto !important;
    transform: translateX(-50%) !important;
  }
</style>
