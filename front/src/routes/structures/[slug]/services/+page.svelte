<script lang="ts">
  import { getStructure } from "$lib/requests/structures";
  import { structure } from "../store";
  import type { PageData } from "./$types";
  import List from "./list.svelte";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
  async function handleRefresh() {
    $structure = await getStructure($structure.slug);
  }
</script>

<List
  servicesOptions={data.servicesOptions}
  serviceStatus={data.serviceStatus}
  updateNeeded={data.updateNeeded}
  structure={$structure}
  total={$structure.services.length}
  onRefresh={handleRefresh}
  withEmptyNotice
/>
