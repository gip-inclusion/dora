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
  import List from "./_list.svelte";

  export let structure, services;
</script>

<svelte:head>
  <title>Services | {structure.name} | DORA</title>
  <meta name="description" content={structure.shortDesc} />
</svelte:head>

<List {services} {structure} />
