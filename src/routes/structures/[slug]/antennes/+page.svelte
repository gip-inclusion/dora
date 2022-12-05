<script lang="ts">
  import { capitalize } from "$lib/utils";
  import { structure } from "../store";
  import List from "./list.svelte";
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
