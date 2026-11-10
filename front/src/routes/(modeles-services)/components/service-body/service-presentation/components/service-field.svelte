<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    title: string;
    children?: Snippet;
  }

  let { title, children }: Props = $props();
</script>

<div>
  <h4 class="text-f16 text-gray-dark mb-s4 leading-24 font-bold">
    {title}
  </h4>
  {@render children?.()}
</div>
