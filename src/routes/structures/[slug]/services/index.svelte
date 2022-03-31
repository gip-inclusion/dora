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
  import { getStructure } from "$lib/structures";

  import List from "./_list.svelte";

  export let structure;

  async function handleRefresh() {
    structure = await getStructure(structure.slug);
  }
</script>

<svelte:head>
  <title>Services | {structure.name} | DORA</title>
  <meta name="description" content={structure.shortDesc} />
</svelte:head>

<List
  services={structure.services || []}
  {structure}
  total={structure.services.length}
  onRefresh={handleRefresh}
/>
