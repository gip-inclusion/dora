<script context="module">
  import { get } from "svelte/store";
  import { userInfo } from "$lib/auth";

  import { getNewModel } from "$lib/components/services/form/utils.js";
  import { getService, getServicesOptions } from "$lib/services";
  import { getStructures } from "$lib/structures";

  export async function load({ url }) {
    const serviceSlug = url.searchParams.get("service");
    const model = serviceSlug ? await getService(serviceSlug) : getNewModel();
    const user = get(userInfo);
    let structures = [];

    if (user?.isStaff) {
      structures = await getStructures();
    } else if (user) {
      structures = user.structures;
    }

    return {
      props: {
        model,
        servicesOptions: await getServicesOptions(),
        structures,
      },
    };
  }
</script>

<script>
  import { page } from "$app/stores";

  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Fields from "$lib/components/services/form/fields.svelte";
  import ModelNavButtons from "$lib/components/services/form/model-nav-buttons.svelte";
  import Errors from "$lib/components/services/form/errors.svelte";

  import Notice from "$lib/components/notice.svelte";

  export let servicesOptions, structures, model;

  let structure;

  if (structures.length === 1) {
    model.structure = structures[0].slug;
    structure = structures[0];
  } else {
    // si la structure est renseignée dans l'URL, force celle-là
    const structureSlug = $page.url.searchParams.get("structure");
    if (structureSlug) {
      structure = structures.find((s) => s.slug === structureSlug);
      model.structure = structureSlug;
    }
  }

  let errorDiv;

  function onError() {
    errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
  }
</script>

<svelte:head>
  <title>Création d'un modèle | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Création d'un modèle</h1>

    {#if !structures.length}
      <Notice title="Impossible de créer un nouveau modèle" type="error">
        <p class="text-f14">Vous n’êtes rattaché à aucune structure.</p>
      </Notice>
    {/if}
  </CenteredGrid>

  <div bind:this={errorDiv} />
  {#if structures.length}
    <Errors />
    <Fields
      bind:service={model}
      {servicesOptions}
      {structures}
      {structure}
      isModel
    />
    <ModelNavButtons {onError} bind:model />
  {/if}
</EnsureLoggedIn>
