<script context="module">
  import { getStructures } from "$lib/structures";

  export async function load() {
    return {
      props: {
        structures: await getStructures(),
      },
    };
  }
</script>

<script>
  import EnsureStaff from "$lib/components/ensure-staff.svelte";
  import StructuresList from "../_structures-list.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  export let structures;
</script>

<svelte:head>
  <title>Toutes les structures | DORA</title>
</svelte:head>

<EnsureStaff>
  <CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
    <div class="col-span-full col-start-1 text-left">
      <div class="mb-s8">
        <h2>Toutes les structures</h2>
      </div>
      <div class="border-t border-gray-03" />
      <StructuresList {structures} />
    </div>
  </CenteredGrid>
</EnsureStaff>
