<script context="module">
  import { getService } from "$lib/services";

  export async function load({ page, _fetch, _session, _context }) {
    return getService(page.params.slug);
  }
</script>

<script>
  import { onMount } from "svelte";
  import { getServiceOptions } from "$lib/services";

  import { serviceCache } from "../form/_stores.js";

  import FormWrapper from "../form/_form-wrapper.svelte";

  export let service;

  let currentStep;
  let serviceOptions;

  onMount(async () => {
    $serviceCache = service;
    serviceOptions = await getServiceOptions();
  });
</script>

<FormWrapper bind:currentStep modify>
  <svelte:component this={currentStep} {serviceOptions} />
</FormWrapper>
