<script context="module">
  export function load({ error, status }) {
    return {
      props: {
        notFound: status === 404,
        status,
        error,
      },
    };
  }
</script>

<script>
  import { onMount } from "svelte";
  import { browser } from "$app/env";
  import { logException } from "$lib/logger";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  export let status, error, notFound;

  onMount(() => {
    if (browser) {
      plausible(`${status}`, { props: { path: document.location.pathname } });
    }
    if (!notFound) {
      const exc = new Error(error.message);
      exc.stack = error.stack;
      logException(exc, { error });
    }
  });
</script>

<svelte:head>
  <title>Erreur | DORA</title>
</svelte:head>

<CenteredGrid topPadded>
  <div class="wrapper col-span-full col-start-1 mb-s64">
    {#if notFound}
      Cette page n’existe pas.
    {:else}
      Erreur inattendue.
    {/if}
  </div>
</CenteredGrid>
