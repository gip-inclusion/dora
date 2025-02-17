<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();
</script>

<CenteredGrid>
  {@render children?.()}
</CenteredGrid>
