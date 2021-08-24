<script context="module">
  import { getService } from "$lib/services";

  export async function load({ page, _fetch, _session, _context }) {
    return getService(page.params.slug);
  }
</script>

<script>
  import { onMount } from "svelte";

  import { getServiceOptions } from "$lib/services";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";

  import ServiceFormWrapper from "../form/_service-form-wrapper.svelte";

  import Step1 from "../form/_step1.svelte";
  import Step2 from "../form/_step2.svelte";
  import Step3 from "../form/_step3.svelte";
  import Step4 from "../form/_step4.svelte";

  export let service;

  let currentStep;
  let serviceOptions;

  const steps = new Map([
    [1, Step1],
    [2, Step2],
    [3, Step3],
    [4, Step4],
  ]);

  onMount(async () => {
    serviceOptions = (await getServiceOptions()).result;
  });

  $: currentStepComponent = steps.get(currentStep);
</script>

<EnsureLoggedIn>
  {#if serviceOptions}
    <ServiceFormWrapper
      bind:currentStep
      bind:service
      modify
      title="Modifier un service">
      <svelte:component
        this={currentStepComponent}
        bind:service
        {serviceOptions} />
    </ServiceFormWrapper>
  {/if}
</EnsureLoggedIn>
