<script context="module">
  import { getServicesOptions } from "$lib/services";

  export async function load({ fetch, url }) {
    const query = url.searchParams;
    const source = query.get("utm_source");

    return {
      props: {
        servicesOptions: await getServicesOptions({ kitFetch: fetch }),
        source,
      },
    };
  }
</script>

<script>
  import FormWrapper from "./form/_form-wrapper.svelte";

  export let servicesOptions, source;
</script>

<svelte:head>
  <title>Contribuer | DORA</title>
</svelte:head>

<FormWrapper {servicesOptions} {source} />
