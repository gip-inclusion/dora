<script lang="ts">
  interface Props {
    condition?: boolean;
    children?: import("svelte").Snippet;
  }

  let { condition = true, children }: Props = $props();
</script>

{#if condition}
  <div class="mb-s16 pl-s16">
    {@render children?.()}
  </div>
{/if}
