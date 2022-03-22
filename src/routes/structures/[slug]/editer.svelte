<script context="module">
  import { getStructure, getStructuresOptions } from "$lib/structures";

  export async function load({ params }) {
    return {
      props: {
        structure: await getStructure(params.slug),
        structuresOptions: await getStructuresOptions(),
      },
    };
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import StructureFormWrapper from "$lib/components/structures/form-wrapper.svelte";

  export let structure, structuresOptions;
</script>

<svelte:head>
  <title>{structure.name} | Éditer | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <div class="col-span-8 col-start-1 mb-s32">
    <StructureFormWrapper
      {structure}
      {structuresOptions}
      modify
      formTitle="Informations"
      visible
    />
  </div>
</EnsureLoggedIn>
