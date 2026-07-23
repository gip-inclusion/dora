<script lang="ts">
  import { page } from "$app/stores";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { RATE_LIMIT_MESSAGE } from "$lib/consts";

  const notFound = $page.status === 404;
  const forbidden = $page.status === 403;
  const rateLimit = $page.status === 429;
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
