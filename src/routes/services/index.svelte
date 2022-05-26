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
  <CenteredGrid --col-bg="var(--col-gray-00)">
    <h1>Services</h1>

    <hr class="border-t border-gray-03" />

    <ServicesList
      {services}
      onRefresh={handleRefresh}
      showStructure
      readOnly={!$userInfo?.isStaff}
    />
  </CenteredGrid>
</EnsureStaffOrBizdev>
