<script context="module">
  import { get } from "svelte/store";
  import { userInfo } from "$lib/auth";

  import {
    createModelFromService,
    getNewModel,
  } from "$lib/components/services/form/utils.js";
  import { getService, getServicesOptions } from "$lib/services";
  import { getStructures } from "$lib/structures";

  export async function load({ url }) {
    const serviceSlug = url.searchParams.get("service");
    const structureSlug = url.searchParams.get("structure");

    const user = get(userInfo);
    let structures = [];

    if (user?.isStaff) {
      structures = await getStructures();
    } else if (user) {
      structures = user.structures;
    }

    let model;

    if (serviceSlug) {
      const service = await getService(serviceSlug);
      model = createModelFromService(service);
      model.slug = null;
      model.structure = null;
      model.service = serviceSlug;
    } else {
      model = getNewModel();
    }

    let structure;

    if (structures.length === 1) {
      model.structure = structures[0].slug;
      structure = structures[0];
    } else if (structureSlug) {
      structure = structures.find((s) => s.slug === structureSlug);
      model.structure = structureSlug;
    }

    return {
      props: {
        model,
        servicesOptions: await getServicesOptions({ model }),
        structures,
        structure,
        serviceSlug,
      },
    };
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Notice from "$lib/components/notice.svelte";
  import ModelFields from "$lib/components/services/form/model-fields.svelte";

  export let servicesOptions, structures, model, structure, serviceSlug;
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
