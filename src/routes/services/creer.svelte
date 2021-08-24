<script>
  import { onMount } from "svelte";
  import { getServiceOptions } from "$lib/services";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";

  import { getNewService } from "./form/_stores.js";
  import ServiceFormWrapper from "./form/_service-form-wrapper.svelte";

  import Step1 from "./form/_step1.svelte";
  import Step2 from "./form/_step2.svelte";
  import Step3 from "./form/_step3.svelte";
  import Step4 from "./form/_step4.svelte";

  let currentStep;
  let serviceOptions;
  let service = getNewService();

  onMount(async () => {
    serviceOptions = (await getServiceOptions()).result;
  });

  const steps = new Map([
    [1, Step1],
    [2, Step2],
    [3, Step3],
    [4, Step4],
  ]);

  $: currentStepComponent = steps.get(currentStep);
</script>

<EnsureLoggedIn>
  {#if serviceOptions}
    <ServiceFormWrapper
      bind:currentStep
      bind:service
      title="Ajouter un service"
      useLocalStorage>
      <svelte:component
        this={currentStepComponent}
        bind:service
        {serviceOptions} />
    </ServiceFormWrapper>
  {/if}
</EnsureLoggedIn>
