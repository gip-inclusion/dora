<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;
  import { getStructure } from "$lib/structures";

  import { capitalize } from "$lib/utils";
  import { structure } from "../_store";

  import List from "./_list.svelte";

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
