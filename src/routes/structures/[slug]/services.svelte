<script context="module">
  export async function load({ stuff }) {
    return {
      props: {
        structure: stuff.structure,
        services: stuff.services,
      },
    };
  }
</script>

<script>
  import AllServices from "./_all_services.svelte";

  export let structure, services;
</script>

<svelte:head>
  <title>Les services | {structure.name} | DORA</title>
  <meta name="description" content={structure.shortDesc} />
</svelte:head>

<AllServices {services} />
