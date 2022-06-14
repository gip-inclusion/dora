<script context="module">
  import { get } from "svelte/store";
  import { userInfo } from "$lib/auth";

  import { getLastDraft, getModel, getServicesOptions } from "$lib/services";

  import { getNewService } from "$lib/components/services/form/utils.js";
  import { getStructures } from "$lib/structures";

  export async function load({ url }) {
    const query = url.searchParams;
    const structureSlug = query.get("structure");
    const modelSlug = query.get("modele");

    const user = get(userInfo);
    let structures = [];

    if (user?.isStaff) {
      structures = await getStructures();
    } else if (user) {
      structures = user.structures;
    }

    let service;
    let model;

    if (modelSlug) {
      model = await getModel(modelSlug);
      service = JSON.parse(JSON.stringify(model));
      service.model = modelSlug;
      service.structure = null;
      service.slug = null;
    } else {
      service = getNewService();
    }

    let structure;

    if (structures.length === 1) {
      service.structure = structures[0].slug;
      structure = structures[0];
    } else if (structureSlug) {
      // si la structure est renseignée dans l'URL, force celle-là
      structure = structures.find((s) => s.slug === structureSlug);
      service.structure = structureSlug;
    }

    return {
      props: {
        lastDraft: await getLastDraft(),
        servicesOptions: await getServicesOptions(),
        structures,
        structure,
        service,
        model,
      },
    };
  }
</script>

<script>
  import { goto } from "$app/navigation";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Fields from "$lib/components/services/form/fields.svelte";
  import ServiceNavButtons from "$lib/components/services/form/service-nav-buttons.svelte";
  import Errors from "$lib/components/services/form/errors.svelte";
  import Notice from "$lib/components/notice.svelte";
  import Button from "$lib/components/button.svelte";

  export let servicesOptions, structures, lastDraft, service, structure, model;

  if (service.structure && lastDraft?.structure !== service.structure) {
    lastDraft = null;
  }

  function handleOpenLastDraft() {
    goto(`/services/${lastDraft.slug}/editer`);
  }

  let errorDiv;

  function onError() {
    errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
  }
</script>

<svelte:head>
  <title>Création d'un service | DORA</title>
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

  <div bind:this={errorDiv} />
  {#if structures.length}
    <Errors />
    <Fields bind:service {servicesOptions} {structures} {structure} {model} />
    <ServiceNavButtons {onError} bind:service />
  {/if}
</EnsureLoggedIn>
