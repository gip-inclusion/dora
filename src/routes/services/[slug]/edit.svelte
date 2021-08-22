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

  import { serviceCache } from "../form/_stores.js";

  import FormWrapper from "../form/_form-wrapper.svelte";

  export let service;

  let currentStep;
  let serviceOptions;

  onMount(async () => {
    $serviceCache = service;
    serviceOptions = (await getServiceOptions()).result;
  });
</script>

<EnsureLoggedIn>
  {#if serviceOptions}
    <FormWrapper bind:currentStep modify title="Modifier un service">
      <svelte:component this={currentStep} {serviceOptions} />
    </FormWrapper>
  {/if}
</EnsureLoggedIn>
