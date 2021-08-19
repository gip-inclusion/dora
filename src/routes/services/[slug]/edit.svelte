<script context="module">
  import { getService } from "$lib/services";

  export async function load({ page, _fetch, _session, _context }) {
    return getService(page.params.slug);
  }
</script>

<script>
  import { onMount } from "svelte";

  import { getApiURL } from "$lib/utils";
  import { token } from "$lib/auth";

  import { serviceCache } from "../form/_stores.js";

  import FormWrapper from "../form/_form-wrapper.svelte";

  export let service;

  let currentStep;
  let serviceOptions;

  onMount(async () => {
    $serviceCache = service;

    const url = `${getApiURL()}/services/`;
    const res = await fetch(url, {
      method: "OPTIONS",
      headers: {
        Accept: "application/json; version=1.0",
        Authorization: `Token ${$token}`,
      },
    });

    if (res.ok) {
      serviceOptions = (await res.json()).actions.POST;
    }

    return {
      status: res.status,
      error: new Error(`Could not load ${url}`),
    };
  });
</script>

<FormWrapper bind:currentStep modify>
  <svelte:component this={currentStep} {serviceOptions} />
</FormWrapper>
