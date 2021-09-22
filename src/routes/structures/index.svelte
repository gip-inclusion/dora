<script context="module">
  import { getStructures } from "$lib/structures";

  export async function load({ _page, _fetch, _session, _context }) {
    return {
      props: {
        structures: await getStructures(),
      },
    };
  }
</script>

<script>
  import StructuresList from "$lib/components/structures-list.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  export let structures;
</script>

<CenteredGrid --col-bg="var(--col-gray-00)">
  <div class="col-start-1 col-span-full text-left">
    <div class="mb-4">
      <h2>Structures</h2>
    </div>
    <div class="border-t border-gray-03 py-3/2" />
  </div>
</CenteredGrid>

<StructuresList {structures} />
