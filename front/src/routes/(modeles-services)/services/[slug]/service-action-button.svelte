<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    ariaLabel: string;
    onclick: () => void;
    children?: Snippet;
  }

  let { ariaLabel, onclick, children }: Props = $props();
</script>

<button
  class="border-gray-03 text-gray-text-alt py-s12 px-s20 hover:text-magenta-cta hover:border-magenta-cta rounded-sm border-1"
  aria-label={ariaLabel}
  {onclick}
>
  {@render children?.()}
</button>
