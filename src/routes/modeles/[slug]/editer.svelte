<script context="module">
  import { get } from "svelte/store";
  import { browser } from "$app/env";

  import { userInfo } from "$lib/auth";
  import { getServicesOptions, getModel } from "$lib/services";
  import { getStructure, getStructures } from "$lib/structures";

  export async function load({ params }) {
    const user = get(userInfo);
    const model = await getModel(params.slug);
    let structure = {};
    let structures = [];
    const servicesOptions = await getServicesOptions();

    // on ne retourne une 404 que sur le client
    if (!browser) {
      return { structure, structures, model, servicesOptions };
    }

    if (!model) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    structure = await getStructure(model.structure);

    if (user.isStaff) {
      structures = await getStructures();
    } else if (user) {
      structures = user.structures;
    }

    return {
      props: {
        model,
        servicesOptions,
        structures,
        structure,
      },
    };
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import Fields from "$lib/components/services/form/fields.svelte";
  import ModelNavButtons from "$lib/components/services/form/model-nav-buttons.svelte";
  import Errors from "$lib/components/services/form/errors.svelte";

  export let model, servicesOptions, structures, structure;

  let errorDiv;

  function onError() {
    errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
  }
</script>

<svelte:head>
  <title>Éditer | {model?.name} | {structure?.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Modification du modèle</h1>
  </CenteredGrid>

  {#if model}
    <div bind:this={errorDiv} />
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
