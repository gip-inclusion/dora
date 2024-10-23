<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import ModelEditionForm from "../../model-edition-form.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Modification du modèle</h1>

    {#if data.model.numServices}
      {@const hasMultipleServices = data.model.numServices > 1}
      <Notice
        title={`Ce modèle est utilisé par ${
          hasMultipleServices ? data.model.numServices : "un"
        } service${hasMultipleServices ? "s" : ""}`}
        type="warning"
      >
        <p class="text-f14">
          Les modifications seront proposées sur tous les services utilisant ce
          modèle.
        </p>
      </Notice>
    {/if}
  </CenteredGrid>

  <ModelEditionForm
    model={data.model}
    servicesOptions={data.servicesOptions}
    structures={data.structures}
    structure={data.structure}
  />
</EnsureLoggedIn>
