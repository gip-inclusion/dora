<script context="module">
  import { getStructure, getStructuresOptions } from "$lib/structures";

  export async function load({ page, _fetch, _session, _context }) {
    return {
      props: {
        structure: await getStructure(page.params.slug),
        structuresOptions: await getStructuresOptions(),
      },
    };
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import StructureFormWrapper from "$lib/components/structures/form-wrapper.svelte";

  export let structure, structuresOptions;
</script>

<svelte:head>
  <title>Éditer ma structure | {structure.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid roundedbg topPadded>
    <div class="col-span-8 col-start-1 mb-s32">
      <StructureFormWrapper
        {structure}
        {structuresOptions}
        modify
        formTitle="Modifiez votre structure"
        visible
      />
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
