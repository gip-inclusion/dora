<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import StaticMarkdown from "$lib/components/display/static-markdown.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<CenteredGrid>
  <StaticMarkdown content={data.content} />
</CenteredGrid>
