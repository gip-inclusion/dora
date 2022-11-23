<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  let { model, servicesOptions, structures, structure, serviceSlug } = data;

  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Notice from "$lib/components/notice.svelte";
  import ModelFields from "$lib/components/services/form/model-fields.svelte";
</script>

<svelte:head>
  <title>Création d'un modèle | DORA</title>
  <meta name="robots" content="noindex" />
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Création d'un modèle</h1>

    {#if !structures.length}
      <Notice title="Impossible de créer un nouveau modèle" type="error">
        <p class="text-f14">Vous n’êtes rattaché à aucune structure.</p>
      </Notice>
    {/if}
    {#if serviceSlug}
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

  <ModelFields {servicesOptions} {structures} {model} {structure} />
</EnsureLoggedIn>
