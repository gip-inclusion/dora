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
  import { userInfo } from "$lib/auth";
  import StructuresList from "./_structures-list.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import EnsureStaffOrBizdev from "$lib/components/ensure-staff-or-bizdev.svelte";
  export let structures;
</script>

<svelte:head>
  <title>Structures | DORA</title>
</svelte:head>

<EnsureStaffOrBizdev>
  <CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
    <div class="col-span-full col-start-1 text-left">
      <div class="mb-s8">
        <h1>Structures</h1>
      </div>
      <StructuresList {structures} readOnly={!$userInfo?.isStaff} />
    </div>
  </CenteredGrid>
</EnsureStaffOrBizdev>
