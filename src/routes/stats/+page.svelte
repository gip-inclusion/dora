<script lang="ts">
  import CG from "$lib/components/display/centered-grid.svelte";
  import { METABASE_EMBED_URL, PLAUSIBLE_EMBED_URL } from "$lib/env";
  import { iframeResize } from "iframe-resizer";

  function hR(id) {
    iframeResize({}, id);
  }
</script>

<svelte:head>
  <script src="https://plausible.io/js/embed.host.js"></script>
</svelte:head>

<CG>
  <div class="text-center">
    <h1 class="text-france-blue">Statistiques</h1>
  </div>
</CG>

<CG>
  <h2>Statistiques d’usage</h2>

  <iframe
    title="Dashboard Plausible"
    src={PLAUSIBLE_EMBED_URL}
    frameborder="0"
    allowtransparency
    on:load={hR("#plausibleIframe")}
    id="plausibleIframe"
  />

  <h2>Statistiques de référencement</h2>

  <iframe
    title="Dashboard Metabase"
    src={METABASE_EMBED_URL}
    frameborder="0"
    allowtransparency
    on:load={hR("#metabaseIframe")}
    id="metabaseIframe"
  />
</CG>

<style lang="postcss">
  iframe {
    width: 100%;
  }

  h2 {
    @apply mb-s0 mt-s20 text-f28;
  }
</style>
