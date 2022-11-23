<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  let {
    servicesOptions,
    serviceStatus,
    updateStatus,
  }: {
    servicesOptions: ServicesOptions;
    serviceStatus: SERVICE_STATUSES | undefined;
    updateStatus: SERVICE_UPDATE_STATUS | undefined;
  } = data;
  import { getStructure } from "$lib/structures";
  import type {
    ServicesOptions,
    SERVICE_STATUSES,
    SERVICE_UPDATE_STATUS,
  } from "$lib/types";
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
  {servicesOptions}
  {serviceStatus}
  {updateStatus}
  structure={$structure}
  total={$structure.services.length}
  onRefresh={handleRefresh}
/>
