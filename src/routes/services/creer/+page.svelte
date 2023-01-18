<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import ServiceEditionForm from "../service-edition-form.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

  if (
    data.service.structure &&
    data.lastDraft?.structure !== data.service.structure
  ) {
    data.lastDraft = null;
  }

  function handleOpenLastDraft() {
    goto(`/services/${data.lastDraft.slug}/editer`);
  }
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Création d'un service</h1>

    {#if !data.structures.length}
      <Notice title="Impossible de créer un nouveau service" type="error">
        <p class="text-f14">Vous n’êtes rattaché à aucune structure.</p>
      </Notice>
    {:else if data.lastDraft}
      <Notice
        title="Vous n’avez pas finalisé votre précédente saisie"
        hasCloseButton
      >
        <p class="text-f14">Souhaitez-vous continuer la saisie du service ?</p>

        <Button
          on:click={handleOpenLastDraft}
          slot="button"
          small
          secondary
          label="Reprendre"
        />
      </Notice>
    {/if}
  </CenteredGrid>

  <ServiceEditionForm
    service={data.service}
    servicesOptions={data.servicesOptions}
    structures={data.structures}
    structure={data.structure}
    model={data.model}
  />
</EnsureLoggedIn>
