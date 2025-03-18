<script lang="ts">
  import { randomId } from "$lib/utils/random";
  import Button from "./button.svelte";

  export let text: string;

  const defaultHeight = 240;
  const id = `text-clamp-${randomId()}`;

  let showAll = false;
  let height: number;

  function toggle() {
    showAll = !showAll;
  }

  $: textIsTooLong = height + 100 > defaultHeight;
  $: label = showAll ? "Réduire" : "Lire la suite";
</script>

<div class="hidden print:inline">
  <div class="prose mb-s24">{@html text}</div>
</div>
<div class="print:hidden">
  <div {id} class:h-s112={!showAll} class="relative overflow-hidden">
    <div class="prose mb-s12" bind:clientHeight={height}>
      {@html text}
    </div>
    {#if !showAll && textIsTooLong}
      <div
        class="bottom-s0 left-s0 h-s112 absolute w-full bg-gradient-to-b from-transparent to-white"
      />
    {/if}
  </div>

  {#if textIsTooLong}
    <Button
      ariaAttributes={{
        "aria-expanded": showAll,
        "aria-controls": id,
      }}
      {label}
      on:click={toggle}
      noBackground
      small
      noPadding
    />
  {/if}
</div>
