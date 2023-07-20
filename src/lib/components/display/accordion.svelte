<script lang="ts">
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import { randomId } from "$lib/utils/random";

  export let title: string;
  export let subTitle = "";
  export let expanded = true;
  export let titleClass = "";
  export let noTitleMargin = false;
  export let titleLevel: "h2" | "h3" | "h4" = "h2";

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
    on:click|preventDefault={() => (expanded = !expanded)}
  >
    <span>
      {title}
      {#if subTitle}
        <span class="-mt-s4 block text-f14 font-normal text-gray-text-alt2">
          {subTitle}
        </span>
      {/if}
    </span>

    <span class="ml-s10 h-s24 w-s24 fill-current text-magenta-cta print:hidden">
      {#if expanded}
        {@html arrowUpSIcon}
      {:else}
        {@html arrowDownSIcon}
      {/if}
    </span>
  </button>
</svelte:element>

<div {id} class:hidden={!expanded}><slot /></div>
