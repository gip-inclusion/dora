<script context="module">
  import { getServices } from "$lib/services";

  export async function load() {
    return {
      props: {
        services: await getServices(),
      },
    };
  }
</script>

<script>
  import { userInfo } from "$lib/auth";

  import EnsureStaffOrBizdev from "$lib/components/ensure-staff-or-bizdev.svelte";
  import ServicesList from "./_services-list.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  export let services;

  async function handleRefresh() {
    services = await getServices();
  }
</script>

<svelte:head>
  <title>Services | DORA</title>
</svelte:head>

<EnsureStaffOrBizdev>
  <CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
    <div class="col-span-full col-start-1 text-left">
      <h2>Services</h2>

      <div class="mb-s16 border-t border-gray-03" />
      <ServicesList
        {services}
        onRefresh={handleRefresh}
        showStructure
        readOnly={!$userInfo?.isStaff}
      />
    </div>
  </CenteredGrid>
</EnsureStaffOrBizdev>
