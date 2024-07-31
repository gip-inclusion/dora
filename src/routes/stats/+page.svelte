<script lang="ts">
  import iframeResize from "@iframe-resizer/parent";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";

  import { METABASE_EMBED_URL } from "$lib/env";
</script>

<CenteredGrid>
  <iframe
    title="Dashboard Metabase"
    src={METABASE_EMBED_URL}
    allowtransparency
    on:load={() => iframeResize({ license: "GPLv3" }, "#metabaseIframe")}
    id="metabaseIframe"
    class="w-full border-0"
  />
</CenteredGrid>
