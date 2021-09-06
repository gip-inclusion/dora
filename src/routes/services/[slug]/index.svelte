<script context="module">
  import { getService } from "$lib/services";

  export async function load({ page, _fetch, _session, _context }) {
    return {
      props: {
        service: await getService(page.params.slug),
      },
    };
  }
</script>

<script>
  import ServiceCard from "./_service-card.svelte";

  export let service;
</script>

<svelte:head>
  <title>Dora: {service?.name} par {service?.structureInfo.name}</title>
</svelte:head>

{#if service}
  <ServiceCard {service} />
{:else}
  <!-- TODO: 404 -->
{/if}
