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
  import { userPreferences } from "$lib/utils/preferences";
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

      if (
        userStructure &&
        $userPreferences.visitedStructures[0] !== userStructureSlug
      ) {
        const updatedVisitedStructures =
          $userPreferences.visitedStructures.filter(
            (slug) => slug !== userStructureSlug
          );
        updatedVisitedStructures.unshift(userStructureSlug);

        localStorage.setItem(
          "visitedStructures",
          JSON.stringify(updatedVisitedStructures)
        );

        userPreferences.set({ visitedStructures: updatedVisitedStructures });

        toast.push({
          msg: `Votre structure active a été automatiquement modifiée : vous utilisez désormais ${userStructure.name}. Attention : si d'autres onglets DORA sont ouverts dans votre navigateur, votre activité dans ces onglets sera également associée à la structure ${userStructure.name}.`,
          duration: 6000,
        });
      }
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
