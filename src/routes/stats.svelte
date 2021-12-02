<script>
  import CG from "$lib/components/layout/centered-grid.svelte";

  function hR() {
    iFrameResize({}, "#myIframe");
  }
</script>

<style>
  iframe {
    width: 100%;
  }
</style>

<svelte:head>
  <title>Statistiques | DORA</title>
  <script
    src="https://metabase.dora.fabrique.social.gouv.fr/app/iframeResizer.js">
  </script>
</svelte:head>

<CG>
  <div class="text-center col-span-full">
    <h1 class="text-france-blue">Statistiques</h1>
  </div>
</CG>

<CG>
  <iframe
    class="col-span-full"
    title="Dashboard Metabase"
    src="https://metabase.dora.fabrique.social.gouv.fr/public/dashboard/9f65d982-fe2e-48f6-bb41-b829b89c29f9#bordered=false&titled=false"
    frameborder="0"
    allowtransparency
    on:load={hR}
    id="myIframe"
  />
</CG>
