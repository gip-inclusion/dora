<script lang="ts">
  import { preventDefault } from "svelte/legacy";

  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import { randomId } from "$lib/utils/random";

  interface Props {
    title: string;
    subTitle?: string;
    expanded?: boolean;
    titleClass?: string;
    noTitleMargin?: boolean;
    titleLevel?: "h2" | "h3" | "h4";
    children?: import("svelte").Snippet;
  }

  let {
    title,
    subTitle = "",
    expanded = $bindable(true),
    titleClass = "",
    noTitleMargin = false,
    titleLevel = "h2",
    children,
  }: Props = $props();

  const id = randomId();
</script>

<svelte:element
  this={titleLevel}
  class="{titleClass} {noTitleMargin ? 'mb-s0' : 'mb-s40'}"
>
  <button
    aria-expanded={expanded}
    aria-controls={id}
    class="flex h-[45px] w-full items-center justify-between text-left"
    onclick={preventDefault(() => (expanded = !expanded))}
  >
    <span>
      {title}
      {#if subTitle}
        <span class="-mt-s4 text-f14 text-gray-text-alt2 block font-normal">
          {subTitle}
        </span>
      {/if}
    </span>

    <span class="ml-s10 h-s24 w-s24 text-magenta-cta fill-current print:hidden">
      {#if expanded}
        {@html arrowUpSIcon}
      {:else}
        {@html arrowDownSIcon}
      {/if}
    </span>
  </button>
</svelte:element>

<div {id} class:hidden={!expanded}>{@render children?.()}</div>
