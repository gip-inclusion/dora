<script context="module">
  import { getServicesOptions } from "$lib/services";

  export async function load({ _page, _fetch, _session, _context }) {
    return {
      props: {
        servicesOptions: await getServicesOptions(),
      },
    };
  }
</script>

<script>
  import Landing from "./_homepage/_landing.svelte";

  export let servicesOptions;
</script>

<Landing {servicesOptions} />
