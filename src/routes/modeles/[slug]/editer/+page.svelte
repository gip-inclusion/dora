<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  let { model, servicesOptions, structures, structure } = data;
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Notice from "$lib/components/notice.svelte";
  import ModelFields from "$lib/components/services/form/model-fields.svelte";

  let multipleServices = 0;

  $: multipleServices = model?.numServices > 1;
</script>

<svelte:head>
  <title>Éditer | {model?.name} | {structure?.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Modification du modèle</h1>

    {#if model.numServices}
      <Notice
        title={`Ce modèle est utilisé par ${
          multipleServices ? model.numServices : "un"
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

  <ModelFields {servicesOptions} {structures} {model} {structure} />
</EnsureLoggedIn>
