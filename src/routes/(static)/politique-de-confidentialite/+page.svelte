<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import StaticMarkdown from "$lib/components/display/static-markdown.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<CenteredGrid>
  <div class="mb-s48">
    <Breadcrumb currentLocation="privacy" dark />
  </div>

  <StaticMarkdown content={data.content} />
</CenteredGrid>
