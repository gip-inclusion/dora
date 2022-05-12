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

  export let servicesOptions;
</script>

<svelte:head>
  <title>Contribuer | DORA</title>
</svelte:head>

<FormWrapper {servicesOptions} />
