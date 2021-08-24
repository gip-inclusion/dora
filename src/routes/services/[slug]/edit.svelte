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

  export let service;

  let currentStep;
  let serviceOptions;

  onMount(async () => {
    serviceOptions = (await getServiceOptions()).result;
  });
</script>

<EnsureLoggedIn>
  {#if serviceOptions}
    <ServiceFormWrapper
      bind:currentStep
      bind:service
      modify
      noLocalStorage
      title="Modifier un service">
      <svelte:component this={currentStep} bind:service {serviceOptions} />
    </ServiceFormWrapper>
  {/if}
</EnsureLoggedIn>
