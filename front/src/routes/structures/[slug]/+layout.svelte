<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Header from "./header.svelte";

  import { structure } from "./store";
  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();
</script>

<CenteredGrid bgColor="bg-magenta-brand print:bg-white" noPadding>
  <Header structure={$structure} />
</CenteredGrid>

<CenteredGrid roundedColor="bg-magenta-brand">
  {@render children?.()}
</CenteredGrid>
