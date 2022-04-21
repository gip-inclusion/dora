<script>
  import List from "./_list.svelte";

  import { structure } from "../_store";
</script>

<svelte:head>
  <title>Antennes | {$structure.name} | DORA</title>
  <meta name="description" content={$structure.shortDesc} />
</svelte:head>

<List
  branches={$structure.branches}
  structure={$structure}
  total={$structure.branches.length}
/>
