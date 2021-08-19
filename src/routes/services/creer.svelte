<script>
  import { onMount } from "svelte";

  import { getApiURL } from "$lib/utils";
  import { token } from "$lib/auth";

  import FormWrapper from "./form/_form-wrapper.svelte";

  let currentStep;
  let serviceOptions;

  onMount(async () => {
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

<FormWrapper bind:currentStep>
  <svelte:component this={currentStep} {serviceOptions} />
</FormWrapper>
