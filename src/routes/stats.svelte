<script>
  import CG from "$lib/components/layout/centered-grid.svelte";
  import { METABASE_EMBED_URL, PLAUSIBLE_EMBED_URL } from "$lib/env.js";
  function hR(id) {
    iFrameResize({}, id);
  }
</script>

<svelte:head>
  <title>Statistiques | DORA</title>
  <script
    src="https://metabase.dora.fabrique.social.gouv.fr/app/iframeResizer.js">
  </script>
</svelte:head>

<CG>
  <div class="col-span-full text-center">
    <h1 class="text-france-blue">Statistiques</h1>
  </div>
</CG>

<CG>
  <iframe
    class="col-span-full"
    title="Dashboard Plausible"
    src={PLAUSIBLE_EMBED_URL}
    frameborder="0"
    allowtransparency
    on:load={hR("#plausibleIframe")}
    id="plausibleIframe"
  />

  <script async src="https://plausible.io/js/embed.host.js"></script>

  <iframe
    class="col-span-full"
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
</style>
