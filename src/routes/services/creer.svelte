<script>
  import { onMount } from "svelte";
  import { getServiceOptions } from "$lib/services";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";

  import FormWrapper from "./form/_form-wrapper.svelte";

  let currentStep;
  let serviceOptions;

  onMount(async () => {
    serviceOptions = (await getServiceOptions()).result;
  });
</script>

<EnsureLoggedIn>
  {#if serviceOptions}
    <FormWrapper bind:currentStep title="Ajouter un service">
      <svelte:component this={currentStep} {serviceOptions} />
    </FormWrapper>
  {/if}
</EnsureLoggedIn>
