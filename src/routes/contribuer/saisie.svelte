<script context="module">
  import { getServicesOptions } from "$lib/services";

  export async function load({ fetch }) {
    return {
      props: {
        servicesOptions: await getServicesOptions({ kitFetch: fetch }),
      },
    };
  }
</script>

<script>
  import FormWrapper from "./form/_form-wrapper.svelte";
  import Step1 from "./form/_step1.svelte";
  import Step2 from "./form/_step2.svelte";
  import serviceSchema from "$lib/schemas/service-contrib";

  export let servicesOptions;
  let service = Object.fromEntries(
    Object.entries(serviceSchema).map(([fieldName, props]) => [
      fieldName,
      props.default,
    ])
  );
  let establishment = null;

  let currentStep = 1;

  const steps = new Map([
    [1, Step1],
    [2, Step2],
  ]);

  $: currentStepComponent = steps.get(currentStep);
</script>

<svelte:head>
  <title>Contribuer | DORA</title>
</svelte:head>

<FormWrapper bind:currentStep bind:service>
  <svelte:component
    this={currentStepComponent}
    bind:service
    bind:establishment
    {servicesOptions}
  />
</FormWrapper>
