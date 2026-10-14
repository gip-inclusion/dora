<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    title: string;
    children?: Snippet;
  }

  let { title, children }: Props = $props();
</script>

<div>
  <h3 class="text-f17 text-france-blue mb-s16 leading-24">
    {title}
  </h3>
  {@render children?.()}
</div>
