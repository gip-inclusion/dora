<script context="module">
  import { get } from "svelte/store";

  import { getLastDraft, getServicesOptions } from "$lib/services";
  import { getStructures, getMyStructures } from "$lib/structures";

  import { userInfo } from "$lib/auth";

  export async function load() {
    return {
      props: {
        lastDraft: await getLastDraft(),
        servicesOptions: await getServicesOptions(),
        structures: get(userInfo)?.isStaff
          ? await getStructures()
          : await getMyStructures(),
      },
    };
  }
</script>

<script>
  import { goto } from "$app/navigation";

  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import TempInlineInfo from "$lib/components/temp-inline-info.svelte";

  import { getNewService } from "./form/_stores.js";
  import ServiceFormWrapper from "./form/_service-form-wrapper.svelte";
  import Step1 from "./form/_step1.svelte";
  import Step2 from "./form/_step2.svelte";
  import Step3 from "./form/_step3.svelte";
  import Step4 from "./form/_step4.svelte";
  import Preview from "./form/_preview.svelte";

  export let servicesOptions, structures, lastDraft;

  let service = getNewService();
  if (structures.length === 1) {
    service.structure = structures[0].slug;
  }
  let lastDraftNotificationVisible = true;
  let currentStep = 1;

  const steps = new Map([
    [1, Step1],
    [2, Step2],
    [3, Step3],
    [4, Step4],
    [5, Preview],
  ]);

  function handleOpenLastDraft() {
    goto(`/services/${lastDraft.slug}/editer`);
  }

  function handleHideLastDraftNotification() {
    lastDraftNotificationVisible = false;
  }
  $: currentStepComponent = steps.get(currentStep);

  $: {
    if (currentStep > 1) {
      // avoid displaying lastDraft notification on ulterior steps
      // AND when going back to first step
      lastDraft = null;
    }
  }
</script>

<svelte:head>
  <title>Référencer votre service | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  {#if !structures.length}
    <CenteredGrid topPadded>
      <div class="col-start-1 col-span-full  mb-s48">
        <h4>Vous n’êtes rattaché à aucune structure !</h4>
      </div></CenteredGrid
    >
  {:else}
    {#if lastDraft && lastDraftNotificationVisible}
      <CenteredGrid topPadded>
        <TempInlineInfo
          label="Vous n’avez pas finalisé votre précédente saisie"
          description="Souhaitez-vous continuer la saisie du service « {lastDraft.name} » ?"
          buttonLabel="Reprendre"
          onAction={handleOpenLastDraft}
          onHide={handleHideLastDraftNotification}
        />
      </CenteredGrid>
    {/if}

    <ServiceFormWrapper
      bind:currentStep
      bind:service
      bind:servicesOptions
      title="Référencer un service"
    >
      <svelte:component
        this={currentStepComponent}
        bind:service
        {servicesOptions}
        {structures}
      />
    </ServiceFormWrapper>
  {/if}
</EnsureLoggedIn>
