<script lang="ts">
  import { browser } from "$app/environment";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import ModelBody from "./model-body.svelte";
  import ModelHeader from "./model-header.svelte";
  import ModelToolbar from "./model-toolbar.svelte";
  import { getModel } from "$lib/requests/services";
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
