<script>
  import List from "./_list.svelte";

  import { structure } from "../_store";
  import { capitalize } from "$lib/utils";
</script>

<svelte:head>
  <title>Antennes | {capitalize($structure.name)} | DORA</title>
  <meta name="description" content={$structure.shortDesc} />
</svelte:head>

<List
  branches={$structure.branches}
  structure={$structure}
  total={$structure.branches.length}
/>
