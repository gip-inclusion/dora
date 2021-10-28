<script context="module">
  import { getServicesOptions } from "$lib/services";

  export async function load({ _page, _fetch, _session, _context }) {
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
  <title>DORA : le référentiel de l'offre d’insertion</title>
  <meta
    name="description"
    content="Plateforme publique dédiée au référencement de l’offre d’insertion et à l’identification et l’activation des leviers adaptés aux besoins des bénéficiaires."
  />
</svelte:head>

<Landing {servicesOptions} />
