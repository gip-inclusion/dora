<script lang="ts">
  // TODO: test error pages
  import { page } from "$app/stores";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import { logException } from "$lib/logger";
  import { trackError } from "$lib/utils/plausible";
  import { onMount } from "svelte";

  onMount(() => {
    trackError(`${$page.status}`, document.location.pathname);

    if (!notFound) {
      const exc = new Error($page.error.message);
      exc.stack = $page.error.stack;
      logException(exc, { error: $page.error });
    }
  });

  const notFound = $page.status === 404;
  const forbidden = $page.status === 403;
</script>

<svelte:head>
  <title>Erreur | DORA</title>
</svelte:head>

<CenteredGrid>
  <p>
    {#if notFound}
      Cette page n’existe pas.
    {:else if forbidden}
      Accès réservé
    {:else}
      Erreur inattendue.
    {/if}
  </p>
</CenteredGrid>
