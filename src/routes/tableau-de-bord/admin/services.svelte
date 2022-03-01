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
  import ServicesList from "../_services-list.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  export let services;
</script>

<svelte:head>
  <title>Tous les services | DORA</title>
</svelte:head>

<EnsureStaffOrBizdev>
  <CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
    <div class="col-span-full col-start-1 text-left">
      <div class="mb-s8">
        <h2>Tous les services</h2>
      </div>
      <div class="border-t border-gray-03" />
      <ServicesList {services} showStructure readOnly={!$userInfo?.isStaff} />
    </div>
  </CenteredGrid>
</EnsureStaffOrBizdev>
