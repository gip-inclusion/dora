<script context="module">
  import { get } from "svelte/store";

  import { browser } from "$app/env";
  import { userInfo } from "$lib/auth";
  import { getServicesOptions, getService } from "$lib/services";
  import { getStructures } from "$lib/structures";

  export async function load({ params }) {
    const user = get(userInfo);
    const service = await getService(params.slug);

    let structures = [];

    if (browser && user.isStaff) {
      structures = await getStructures();
    } else if (browser && user) {
      structures = user.structures;
    }

    return {
      props: {
        service,
        servicesOptions: await getServicesOptions(),
        structures,
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

<svelte:head>
  <title>Éditer | {service?.name} | {service?.structureInfo.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  {#if service}
    <ServiceFormWrapper
      bind:currentStep
      bind:service
      bind:servicesOptions
      title="Modifier un service"
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
