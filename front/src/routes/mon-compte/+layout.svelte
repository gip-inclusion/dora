<script lang="ts">
  import type { Snippet } from "svelte";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";

  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();
</script>

<CenteredGrid>
  {@render children?.()}
</CenteredGrid>
