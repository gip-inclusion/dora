<script lang="ts">
  // import { browser } from "$app/environment";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

  let { model, servicesOptions } = data;

  import { onMount } from "svelte";
  import { trackModel } from "$lib/utils/plausible";

  import ModelHeader from "$lib/components/services/model-header.svelte";
  import ModelToolbar from "$lib/components/services/model-toolbar.svelte";
  import ModelBody from "$lib/components/services/model-body.svelte";
  import { getModel } from "$lib/services";
  import { browser } from "$app/environment";

  onMount(() => {
    trackModel(model);
  });

  async function handleRefresh() {
    model = await getModel(model.slug);
  }
</script>

<svelte:head>
  <title>{model?.name} | {model?.structureInfo.name} | DORA</title>
  <meta name="description" content={model?.shortDesc} />
</svelte:head>

<CenteredGrid bgColor="bg-gray-bg">
  <ModelHeader {model} />
</CenteredGrid>
<hr />
<CenteredGrid noPadding>
  <div class="py-s24 print:hidden">
    {#if browser}
      <ModelToolbar {model} onRefresh={handleRefresh} />
    {/if}
  </div>
</CenteredGrid>

<CenteredGrid>
  <ModelBody service={model} {servicesOptions} />
</CenteredGrid>
