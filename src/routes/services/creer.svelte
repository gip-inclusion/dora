<script>
  import { onMount } from "svelte";
  import { getServiceOptions } from "$lib/services";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";

  import { getNewService } from "./form/_stores.js";
  import ServiceFormWrapper from "./form/_service-form-wrapper.svelte";

  let currentStep;
  let serviceOptions;
  let service = getNewService();

  onMount(async () => {
    serviceOptions = (await getServiceOptions()).result;
  });
</script>

<EnsureLoggedIn>
  {#if serviceOptions}
    <ServiceFormWrapper
      bind:currentStep
      bind:service
      title="Ajouter un service">
      <svelte:component this={currentStep} bind:service {serviceOptions} />
    </ServiceFormWrapper>
  {/if}
</EnsureLoggedIn>
