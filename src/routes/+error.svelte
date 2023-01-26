<script lang="ts">
  import { page } from "$app/stores";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { logException } from "$lib/utils/logger";
  import { trackError } from "$lib/utils/plausible";
  import { onMount } from "svelte";

  const notFound = $page.status === 404;
  const forbidden = $page.status === 403;

  onMount(() => {
    trackError(`${$page.status}`, document.location.pathname);

    if (!notFound) {
      logException($page.error);
    }
  });
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
