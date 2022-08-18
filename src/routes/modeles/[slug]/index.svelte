<script context="module">
  import { browser } from "$app/env";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import { getModel } from "$lib/services";

  export async function load({ params, fetch }) {
    const model = await getModel(params.slug, { kitFetch: fetch });

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
      },
    };
  }
</script>

<script>
  import { onMount } from "svelte";
  import ModelHeader from "$lib/components/services/model-header.svelte";
  import ModelToolbar from "$lib/components/services/model-toolbar.svelte";
  import ServiceBody from "$lib/components/services/service-body.svelte";

  export let model;

  onMount(() => {
    if (browser) {
      plausible("model", {
        props: {
          model: model.name,
          slug: model.slug,
          structure: model.structureInfo.name,
          departement: model.department,
        },
      });
    }
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
  <div class="noprint py-s24">
    {#if browser}
      <ModelToolbar {model} onRefresh={handleRefresh} />
    {/if}
  </div>
</CenteredGrid>

<CenteredGrid>
  <ServiceBody service={model} isModel />
</CenteredGrid>
