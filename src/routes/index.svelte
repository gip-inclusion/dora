<script context="module">
  import { getServicesOptions } from "$lib/services";

  export async function load() {
    return {
      props: {
        servicesOptions: await getServicesOptions(),
      },
    };
  }
</script>

<script>
  import Landing from "./_homepage/_landing.svelte";

  export let servicesOptions;
</script>

<svelte:head>
  <title>DORA : recensement et mise à jour de l’offre d’insertion</title>
  <meta
    name="description"
    content="Le service public numérique de recensement et mise à jour de l’offre d’insertion."
  />
</svelte:head>

<Landing {servicesOptions} />
