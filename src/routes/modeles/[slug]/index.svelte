<script context="module">
  import { browser } from "$app/env";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import { getModel, getServicesOptions } from "$lib/services";

  export async function load({ params }) {
    const model = await getModel(params.slug);

    // on ne retourne une 404 que sur le client
    if (!model && !browser) {
      return {};
    }

    if (!model) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    return {
      props: {
        model,
        servicesOptions: await getServicesOptions(),
      },
    };
  }
</script>

<script>
  import { onMount } from "svelte";
  import { trackModel } from "$lib/utils/plausible";

  import ModelHeader from "$lib/components/services/model-header.svelte";
  import ModelToolbar from "$lib/components/services/model-toolbar.svelte";
  import ModelBody from "$lib/components/services/model-body.svelte";

  export let model;
  export let servicesOptions;

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
