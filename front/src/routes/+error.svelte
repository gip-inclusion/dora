<script lang="ts">
  import { page } from "$app/stores";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { RATE_LIMIT_MESSAGE, STALE_CHUNK_RELOAD_MESSAGE } from "$lib/consts";
  import { logException } from "$lib/utils/logger";
  import { onMount } from "svelte";

  const notFound = $page.status === 404;
  const forbidden = $page.status === 403;
  const rateLimit = $page.status === 429;
  // La page va être rechargée automatiquement (voir hooks.client.ts),
  // inutile de remonter l'erreur à Sentry
  const staleChunkReload = $page.error?.message === STALE_CHUNK_RELOAD_MESSAGE;

  onMount(() => {
    if (!notFound && !staleChunkReload) {
      logException(new Error($page.error?.message ?? String($page.status)));
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
    {:else if rateLimit}
      {RATE_LIMIT_MESSAGE}
    {:else}
      Erreur inattendue.
    {/if}
  </p>
</CenteredGrid>
