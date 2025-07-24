<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    selfStart?: boolean;
    bgColorClass?: string;
    textColorClass?: string;
    children?: Snippet;
  }

  let {
    selfStart = false,
    bgColorClass = "bg-gray-text-alt",
    textColorClass = "text-white",
    children,
  }: Props = $props();
</script>

<span
  class="break-word px-s8 py-s2 text-f14 rounded-sm font-bold {textColorClass} {bgColorClass}"
  class:self-start={selfStart}
>
  {@render children?.()}
</span>
