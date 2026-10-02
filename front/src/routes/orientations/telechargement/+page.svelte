<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";

  import ExportDownload from "./export-download.svelte";
  import type { PageData } from "./$types";

  interface Props {
    data: PageData;
  }
  const { data }: Props = $props();
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1 class="mt-s24">Suivi des orientations</h1>
    <ExportDownload
      structureSlug={data.structureSlug}
      type={data.type}
      token={data.token}
    />
  </CenteredGrid>
</EnsureLoggedIn>
