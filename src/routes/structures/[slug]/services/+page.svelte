<script lang="ts">
  import { getStructure } from "$lib/structures";
  import { capitalize } from "$lib/utils";
  import { structure } from "../store";
  import type { PageData } from "./$types";
  import List from "./list.svelte";

  export let data: PageData;
  async function handleRefresh() {
    $structure = await getStructure($structure.slug);
  }
</script>

<svelte:head>
  <title>Services | {capitalize($structure.name)} | DORA</title>
  <meta name="description" content={$structure.shortDesc} />
</svelte:head>

<List
  servicesOptions={data.servicesOptions}
  serviceStatus={data.serviceStatus}
  updateStatus={data.updateStatus}
  structure={$structure}
  total={$structure.services.length}
  onRefresh={handleRefresh}
/>
