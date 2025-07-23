<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();
</script>

<div
  class="bold bg-magenta-dark px-s8 text-f14 inline-block w-fit self-center rounded-full pt-[1px] pb-[3px] leading-[18px] text-white"
>
  {@render children?.()}
</div>
