<script>
  import Button from "./button.svelte";

  export let text = "";

  let showAll = false;
  let label;

  function toggle() {
    showAll = !showAll;
  }

  let textIsTooLong, height;
  const defaultHeight = 240;

  $: textIsTooLong = height + 100 > defaultHeight;
  $: label = showAll ? "Réduire" : "Lire la suite";
</script>

<div class:h-s160={!showAll} class="relative mb-s24 overflow-hidden">
  <div class="prose mb-s24" bind:clientHeight={height}>{@html text}</div>
  <div class:gradient={!showAll} />
</div>

{#if textIsTooLong}
  <Button {label} on:click={toggle} noBackground small noPadding />
{/if}

<style>
  .gradient {
    position: absolute;
    bottom: 0px;
    left: 0px;
    width: 100%;
    height: 100px;
    background: linear-gradient(
      to bottom,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 1) 100%
    ); /* W3C */
  }
</style>
