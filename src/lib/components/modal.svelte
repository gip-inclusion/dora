<script>
  import { browser } from "$app/env";
  import { closeLineIcon } from "$lib/icons";
  import Button from "./button.svelte";

  export let isOpen;
  export let overflow = false;
  export let title = undefined;

  $: {
    // Prevent scrolling the background while the modal is open
    if (browser) {
      document.body.style.overflow = isOpen ? "hidden" : "visible";
    }
  }

  function handleKeydown(event) {
    if (event.key === "Escape") isOpen = false;
  }

  function handleBackgroundClick() {
    isOpen = false;
  }
  function handleClose() {
    isOpen = false;
  }
</script>

<svelte:window on:keydown={handleKeydown} />

<div
  id="background"
  class="flex items-center justify-center"
  class:hidden={!isOpen}
  on:click={handleBackgroundClick}
>
  <div
    class="max-h-screen min-w-[80vw] rounded-md bg-white p-s24 shadow-md"
    class:overflow-y-auto={overflow}
    on:click|stopPropagation
  >
    <div class="mb-s24 flex justify-between">
      {#if title}
        <h2>{title}</h2>
      {/if}

      <div class="ml-auto">
        <Button
          icon={closeLineIcon}
          on:click={handleClose}
          noBackground
          secondary
        />
      </div>
    </div>
    <slot />
  </div>
</div>

<style lang="postcss">
  #background {
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: #000000cc;
  }
</style>
