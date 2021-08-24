<script context="module">
  import { getStructure } from "$lib/structures";

  export async function load({ page, _fetch, _session, _context }) {
    return getStructure(page.params.slug);
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import StructureFormWrapper from "../_structure-form-wrapper.svelte";
  export let structure;
</script>

<svelte:head>
  <title>Dora: {structure.name}</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid roundedbg>
    <div class="col-span-8 col-start-1 mb-4">
      <StructureFormWrapper
        {structure}
        formTitle="Modifiez votre structure"
        modify
        visible />
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
