<script lang="ts">
  import { getStructure } from "$lib/requests/structures";
  import { structure } from "../store";
  import type { PageData } from "./$types";
  import List from "./list.svelte";

  export let data: PageData;
  async function handleRefresh() {
    $structure = await getStructure($structure.slug);
  }
</script>

<List
  servicesOptions={data.servicesOptions}
  serviceStatus={data.serviceStatus}
  updateStatus={data.updateStatus}
  structure={$structure}
  total={$structure.services.length}
  onRefresh={handleRefresh}
/>
