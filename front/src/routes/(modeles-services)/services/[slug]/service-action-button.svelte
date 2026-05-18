<script lang="ts">
  import type { Snippet } from "svelte";

  type Props = {
    ariaLabel: string;
    children?: Snippet;
  } & (
    | { href: string; onclick?: (event: MouseEvent) => void }
    | { href?: never; onclick: (event: MouseEvent) => void }
  );

  let { ariaLabel, onclick, href, children }: Props = $props();

  const classes =
    "border-gray-03 text-gray-text-alt py-s12 px-s20 hover:text-magenta-cta hover:border-magenta-cta rounded-sm border-1 inline-flex items-center justify-center";
</script>

{#if href}
  <a {href} class={classes} aria-label={ariaLabel} {onclick}>
    {@render children?.()}
  </a>
{:else}
  <button class={classes} aria-label={ariaLabel} {onclick}>
    {@render children?.()}
  </button>
{/if}
