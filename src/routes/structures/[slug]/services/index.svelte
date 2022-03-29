<script context="module">
  export async function load({ stuff }) {
    return {
      props: {
        structure: stuff.structure,
      },
    };
  }
</script>

<script>
  import List from "./_list.svelte";

  export let structure;
</script>

<svelte:head>
  <title>Services | {structure.name} | DORA</title>
  <meta name="description" content={structure.shortDesc} />
</svelte:head>

<List
  services={structure.services || []}
  {structure}
  total={structure.services.length}
/>
