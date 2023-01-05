<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import ModelFields from "../model-fields.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Création d'un modèle</h1>

    {#if !data.structures.length}
      <Notice title="Impossible de créer un nouveau modèle" type="error">
        <p class="text-f14">Vous n’êtes rattaché à aucune structure.</p>
      </Notice>
    {/if}
    {#if data.serviceSlug}
      <Notice
        title="Le service utilisé comme base sera synchronisé avec ce modèle"
        type="info"
      >
        <p class="text-f14">
          À chaque mise à jour du modèle, vous pourrez implémenter les
          modifications sur ce service.
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
