<script context="module">
  import { getService } from "$lib/services";

  export async function load({ page, _fetch, _session, _context }) {
    return getService(page.params.slug);
  }
</script>

<script>
  import Step4 from "../../form/_step4.svelte";
  export let service;
</script>

<svelte:head>
  <title>Dora: {service.name}</title>
</svelte:head>

{#if service}
  <Step4 {service} />
{/if}
