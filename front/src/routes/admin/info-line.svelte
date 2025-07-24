<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    condition?: boolean;
    children?: Snippet;
  }

  let { condition = true, children }: Props = $props();
</script>

{#if condition}
  <div class="mb-s16 pl-s16">
    {@render children?.()}
  </div>
{/if}
