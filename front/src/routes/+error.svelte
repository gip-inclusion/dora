<script lang="ts">
  import { page } from "$app/stores";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import {
    RATE_LIMIT_MESSAGE,
    STALE_CHUNK_RELOAD_MESSAGE,
    UNEXPECTED_ERROR_MESSAGE,
  } from "$lib/consts";
  import { logException } from "$lib/utils/logger";
  import { onMount } from "svelte";

  const notFound = $page.status === 404;
  const forbidden = $page.status === 403;
  const rateLimit = $page.status === 429;
  // La page va être rechargée automatiquement (voir hooks.client.ts),
  // inutile de remonter l'erreur à Sentry
  const staleChunkReload = $page.error?.message === STALE_CHUNK_RELOAD_MESSAGE;
  // Les erreurs inattendues sont déjà rapportées à Sentry par handleErrorWithSentry
  // (hooks.client/server.ts), qui masque leur message par UNEXPECTED_ERROR_MESSAGE.
  // Les re-logger ici créerait un doublon regroupé dans un unique bucket de bruit.
  const alreadyReported = $page.error?.message === UNEXPECTED_ERROR_MESSAGE;

  onMount(() => {
    if (!notFound && !staleChunkReload && !alreadyReported) {
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
