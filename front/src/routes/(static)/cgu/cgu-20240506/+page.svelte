<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import StaticMarkdown from "$lib/components/display/static-markdown.svelte";
  import type { PageData } from "./$types";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
</script>

<CenteredGrid>
  <div class="mb-s48">
    <Breadcrumb currentLocation="cgu" />
  </div>

  <StaticMarkdown content={data.content} />
</CenteredGrid>
