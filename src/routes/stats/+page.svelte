<script lang="ts">
  import { iframeResizer } from "iframe-resizer";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";

  import { METABASE_EMBED_URL } from "$lib/env";
</script>

<CenteredGrid>
  <iframe
    title="Dashboard Metabase"
    src={METABASE_EMBED_URL}
    allowtransparency
    on:load={() => iframeResizer({}, "#metabaseIframe")}
    id="metabaseIframe"
    class="w-full border-0"
  />
</CenteredGrid>
