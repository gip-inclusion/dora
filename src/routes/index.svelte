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
    content="Plateforme publique dédiée au référencement de l’offre d’insertion et à l’identification et l’activation des leviers adaptés aux besoins des bénéficiaires."
  />
</svelte:head>

<Landing {servicesOptions} />
