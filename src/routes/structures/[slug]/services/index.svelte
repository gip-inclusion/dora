<script context="module">
  import { getServicesOptions } from "$lib/services";

  export async function load({ url }) {
    const query = url.searchParams;
    return {
      props: {
        serviceStatus: query.get("service-status"),
        updateStatus: query.get("update-status"),
        servicesOptions: await getServicesOptions(),
      },
    };
  }
</script>

<script lang="ts">
  import { getStructure } from "$lib/structures";
  import type {
    ServicesOptions,
    SERVICE_STATUSES,
    SERVICE_UPDATE_STATUS,
  } from "$lib/types.js";
  import { capitalize } from "$lib/utils.js";
  import { structure } from "../_store";

  import List from "./_list.svelte";

  async function handleRefresh() {
    $structure = await getStructure($structure.slug);
  }

  export let servicesOptions: ServicesOptions;
  export let serviceStatus: SERVICE_STATUSES | undefined;
  export let updateStatus: SERVICE_UPDATE_STATUS | undefined;
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
