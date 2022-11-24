<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Notice from "$lib/components/notice.svelte";
  import ModelFields from "$lib/components/services/form/model-fields.svelte";

  let multipleServices = 0;

  $: multipleServices = data.model?.numServices > 1;
</script>

<svelte:head>
  <title>Éditer | {data.model?.name} | {data.structure?.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Modification du modèle</h1>

    {#if data.model.numServices}
      <Notice
        title={`Ce modèle est utilisé par ${
          multipleServices ? data.model.numServices : "un"
        } service${multipleServices ? "s" : ""}`}
        type="warning"
      >
        <p class="text-f14">
          Les modifications seront proposées sur tous les services utilisant ce
          modèle.
        </p>
      </Notice>
    {/if}
  </CenteredGrid>

  <ModelFields
    servicesOptions={data.servicesOptions}
    structures={data.structures}
    model={data.model}
    structure={data.structure}
  />
</EnsureLoggedIn>
