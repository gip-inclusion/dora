<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();
</script>

<ul class="space-y-s2 list-inside list-disc">
  {@render children?.()}
</ul>
