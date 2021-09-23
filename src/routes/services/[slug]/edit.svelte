<script context="module">
  import { getServicesOptions, getService } from "$lib/services";
  import { getMyStructures } from "$lib/structures";

  export async function load({ page, _fetch, _session, _context }) {
    const service = await getService(page.params.slug);
    return {
      props: {
        service,
        servicesOptions: await getServicesOptions(),
        structures: await getMyStructures(),
      },
    };
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";

  import ServiceFormWrapper from "../form/_service-form-wrapper.svelte";

  import Step1 from "../form/_step1.svelte";
  import Step2 from "../form/_step2.svelte";
  import Step3 from "../form/_step3.svelte";
  import Step4 from "../form/_step4.svelte";
  import Preview from "../form/_preview.svelte";

  export let service, servicesOptions, structures;

  let currentStep = 1;

  const steps = new Map([
    [1, Step1],
    [2, Step2],
    [3, Step3],
    [4, Step4],
    [5, Preview],
  ]);
  $: currentStepComponent = steps.get(currentStep);
</script>

<EnsureLoggedIn>
  {#if service}
    <ServiceFormWrapper
      bind:currentStep
      bind:service
      title="Modifier un service">
      <svelte:component
        this={currentStepComponent}
        bind:service
        {servicesOptions}
        {structures} />
    </ServiceFormWrapper>
  {/if}
</EnsureLoggedIn>
