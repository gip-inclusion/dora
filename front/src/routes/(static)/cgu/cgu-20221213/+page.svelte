<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import StaticMarkdown from "$lib/components/display/static-markdown.svelte";
  import type { PageData } from "./$types";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
</script>

<CenteredGrid>
  <StaticMarkdown content={data.content} />
</CenteredGrid>
