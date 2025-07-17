<script lang="ts">
  import { createBubbler } from "svelte/legacy";

  const bubble = createBubbler();
  interface Props {
    ariaLabel: string;
    children?: import("svelte").Snippet;
  }

  let { ariaLabel, children }: Props = $props();
</script>

<button
  class="border-gray-03 text-gray-text-alt py-s12 px-s20 hover:text-magenta-cta hover:border-magenta-cta rounded-sm border-1"
  aria-label={ariaLabel}
  onclick={bubble("click")}
>
  {@render children?.()}
</button>
