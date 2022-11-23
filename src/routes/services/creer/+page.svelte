<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  let { servicesOptions, structures, lastDraft, service, structure, model } =
    data;
  import { goto } from "$app/navigation";

  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import Notice from "$lib/components/notice.svelte";
  import Button from "$lib/components/button.svelte";
  import ServiceFields from "$lib/components/services/form/service-fields.svelte";

  if (service.structure && lastDraft?.structure !== service.structure) {
    lastDraft = null;
  }

  function handleOpenLastDraft() {
    goto(`/services/${lastDraft.slug}/editer`);
  }
</script>

<svelte:head>
  <title>Création d'un service | DORA</title>
  <meta name="robots" content="noindex" />
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Création d'un service</h1>

    {#if !structures.length}
      <Notice title="Impossible de créer un nouveau service" type="error">
        <p class="text-f14">Vous n’êtes rattaché à aucune structure.</p>
      </Notice>
    {:else if lastDraft}
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

  <ServiceFields {service} {servicesOptions} {structures} {structure} {model} />
</EnsureLoggedIn>
