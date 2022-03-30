<script context="module">
  import { getStructuresOptions } from "$lib/structures";

  export async function load({ stuff }) {
    return {
      props: {
        structure: stuff.structure,
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
      bind:structure
      {structuresOptions}
      modify
      formTitle="Informations"
      visible
    />
  </div>
</EnsureLoggedIn>
