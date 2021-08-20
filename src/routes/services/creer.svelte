<script>
  import { onMount } from "svelte";
  import { getServiceOptions } from "$lib/services";

  import FormWrapper from "./form/_form-wrapper.svelte";

  let currentStep;
  let serviceOptions;

  onMount(async () => {
    serviceOptions = (await getServiceOptions()).result;
  });
</script>

{#if serviceOptions}
  <FormWrapper bind:currentStep>
    <svelte:component this={currentStep} {serviceOptions} />
  </FormWrapper>
{/if}
