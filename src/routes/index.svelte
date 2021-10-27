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
  <title>DORA: l’offre de services de l’insertion</title>
  <meta
    name="description"
    content="Service public permettant aux structures de l’insertion de référencer leurs services et aux prescripteurs de trouver le meilleur service pour leur bénéficiaire."
  />
</svelte:head>

<Landing {servicesOptions} />
