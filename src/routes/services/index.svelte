<script context="module">
  import { getServices } from "$lib/services";

  export async function load({ _page, _fetch, _session, _context }) {
    return {
      props: {
        services: await getServices(),
      },
    };
  }
</script>

<script>
  import ServicesList from "$lib/components/services-list.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  export let services;
</script>

<CenteredGrid --col-bg="var(--col-gray-00)">
  <div class="col-start-1 col-span-full text-left">
    <div class="mb-4">
      <h2>Services</h2>
    </div>
    <div class="border-t border-gray-03 py-3/2" />
  </div>
</CenteredGrid>

<ServicesList {services} />
