<script lang="ts">
  import { browser } from "$app/environment";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import ModelBody from "$lib/components/services/model-body.svelte";
  import ModelHeader from "$lib/components/services/model-header.svelte";
  import ModelToolbar from "$lib/components/services/model-toolbar.svelte";
  import { getModel } from "$lib/services";
  import { trackModel } from "$lib/utils/plausible";
  import { onMount } from "svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

  onMount(() => {
    trackModel(data.model);
  });

  async function handleRefresh() {
    data.model = await getModel(data.model.slug);
  }
</script>

<svelte:head>
  <title>{data.model?.name} | {data.model?.structureInfo.name} | DORA</title>
  <meta name="description" content={data.model?.shortDesc} />
</svelte:head>

<CenteredGrid bgColor="bg-gray-bg">
  <ModelHeader model={data.model} />
</CenteredGrid>
<hr />
<CenteredGrid noPadding>
  <div class="py-s24 print:hidden">
    {#if browser}
      <ModelToolbar model={data.model} onRefresh={handleRefresh} />
    {/if}
  </div>
</CenteredGrid>

<CenteredGrid>
  <ModelBody service={data.model} servicesOptions={data.servicesOptions} />
</CenteredGrid>
