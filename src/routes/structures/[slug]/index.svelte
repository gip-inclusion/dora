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
  import LatestServices from "./_latest-services.svelte";
  import StructurePres from "./_structure-pres.svelte";

  export let structure, services;
</script>

<svelte:head>
  <title>{structure.name} | DORA</title>
  <meta name="description" content={structure.shortDesc} />
</svelte:head>

<StructurePres {structure} />
<LatestServices {structure} services={services.slice(0, 3)} />
