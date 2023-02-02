<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { METABASE_EMBED_URL, PLAUSIBLE_EMBED_URL } from "$lib/env";
  import { iframeResize } from "iframe-resizer";

  function handleResize(id: string) {
    iframeResize({}, id);
  }
</script>

<svelte:head />

<CenteredGrid>
  <div class="text-center">
    <h1 class="text-france-blue">Statistiques</h1>
  </div>
</CenteredGrid>

<CenteredGrid>
  <h2>Statistiques d’usage</h2>

  <iframe
    title="Dashboard Plausible"
    src={PLAUSIBLE_EMBED_URL}
    frameborder="0"
    allowtransparency
    on:load={() => handleResize("#plausibleIframe")}
    id="plausibleIframe"
  />

  <h2>Statistiques de référencement</h2>

  <iframe
    title="Dashboard Metabase"
    src={METABASE_EMBED_URL}
    frameborder="0"
    allowtransparency
    on:load={() => handleResize("#metabaseIframe")}
    id="metabaseIframe"
  />
</CenteredGrid>

<style lang="postcss">
  iframe {
    width: 100%;
  }

  h2 {
    @apply mb-s0 mt-s20 text-f28;
  }
</style>
