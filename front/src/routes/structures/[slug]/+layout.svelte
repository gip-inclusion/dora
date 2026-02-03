<script lang="ts">
  import type { Snippet } from "svelte";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Header from "./header.svelte";

  import { structure } from "./store";

  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();
</script>

<CenteredGrid bgColor="bg-magenta-20 print:bg-white" noPadding>
  <Header structure={$structure} />
</CenteredGrid>

<CenteredGrid roundedColor="bg-magenta-20">
  {@render children?.()}
</CenteredGrid>
