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
    const servicesOptions = await getServicesOptions({ model });

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
  import Notice from "$lib/components/notice.svelte";
  import ModelFields from "$lib/components/services/form/model-fields.svelte";

  export let model, servicesOptions, structures, structure;

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
