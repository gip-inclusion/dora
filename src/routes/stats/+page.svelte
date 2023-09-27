<script lang="ts">
  import { iframeResizer } from "iframe-resizer";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";

  import { METABASE_EMBED_URL } from "$lib/env";
</script>

<svelte:head />

<CenteredGrid>
  <div class="text-center">
    <h1 class="text-france-blue">Statistiques</h1>
  </div>
</CenteredGrid>

<CenteredGrid>
  <iframe
    title="Dashboard Metabase"
    src={METABASE_EMBED_URL}
    allowtransparency
    on:load={() => iframeResizer({}, "#metabaseIframe")}
    id="metabaseIframe"
  />
</CenteredGrid>

<style lang="postcss">
  iframe {
    @apply w-full border-0;
  }
</style>
