<script context="module">
  import { getLastDraft, getServicesOptions } from "$lib/services";
  import { getStructures } from "$lib/structures";

  export async function load({ _page, _fetch, _session, _context }) {
    return {
      props: {
        lastDraft: await getLastDraft(),
        servicesOptions: await getServicesOptions(),
        structures: await getStructures(),
      },
    };
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import Label from "$lib/components/label.svelte";

  import { getNewService } from "./form/_stores.js";
  import ServiceFormWrapper from "./form/_service-form-wrapper.svelte";

  import Step1 from "./form/_step1.svelte";
  import Step2 from "./form/_step2.svelte";
  import Step3 from "./form/_step3.svelte";
  import Step4 from "./form/_step4.svelte";
  import Preview from "./form/_preview.svelte";

  export let servicesOptions, structures, lastDraft;

  let service = getNewService();
  let currentStep;

  const steps = new Map([
    [1, Step1],
    [2, Step2],
    [3, Step3],
    [4, Step4],
    [5, Preview],
  ]);

  $: currentStepComponent = steps.get(currentStep);
</script>

<style>
  .draft-wrapper {
    display: flex;
    flex-direction: row;
    grid-column: 1/-1;
  }
</style>

<EnsureLoggedIn>
  {#if lastDraft}
    <CenteredGrid>
      <div class="draft-wrapper">
        <Label>
          <div class="mr-1">
            Voulez vous reprendre votre dernier brouillon “{lastDraft.name}” ?
          </div>
          <LinkButton
            to="/services/{lastDraft.slug}/edit"
            label="Reprendre"
            small /></Label>
      </div>
    </CenteredGrid>
  {/if}

  <ServiceFormWrapper
    bind:currentStep
    bind:service
    title="Référencer un service">
    <svelte:component
      this={currentStepComponent}
      bind:service
      {servicesOptions}
      {structures} />
  </ServiceFormWrapper>
</EnsureLoggedIn>
