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
  export let structure, antennes;
</script>

<svelte:head>
  <title>{structure.name} | Antennes | DORA</title>
  <meta name="description" content={structure.shortDesc} />
</svelte:head>

<List {antennes} {structure} />
