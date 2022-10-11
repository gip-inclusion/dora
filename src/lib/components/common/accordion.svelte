<script lang="ts">
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import { uid } from "uid";

  export let title: string;
  export let expanded = true;

  const id = uid();
</script>

<h2 class="mb-s40">
  <button
    aria-expanded={expanded}
    aria-controls={id}
    class="flex h-[45px] w-full items-center justify-between text-left"
    on:click={() => (expanded = !expanded)}
  >
    {title}

    <span class="ml-s10 h-s24 w-s24 fill-current text-magenta-cta print:hidden">
      {#if expanded}
        {@html arrowUpSIcon}
      {:else}
        {@html arrowDownSIcon}
      {/if}
    </span>
  </button>
</h2>

<div {id} class:hidden={!expanded}><slot /></div>
