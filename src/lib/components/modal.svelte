<script>
  import { browser } from "$app/env";
  import { closeLineIcon } from "$lib/icons";

  export let isOpen;

  $: {
    // Prevent scrolling the background while the modal is open
    if (browser) {
      document.body.style.overflow = isOpen ? "hidden" : "visible";
    }
  }

  function handleKeydown(event) {
    if (event.key === "Escape") isOpen = false;
  }

  function handleClose() {
    isOpen = false;
  }
</script>

<style lang="postcss">
  #background {
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    display: none;
    width: 100vw;
    height: 100vh;
    background-color: black;
    opacity: 0.5;
  }

  #modal {
    position: fixed;
    z-index: 1;
    top: 50%;
    left: 50%;
    display: none;
    max-width: 95vw;
    max-height: 95vh;
    overflow-y: auto;
    transform: translate(-50%, -50%);
  }

  .show {
    display: block !important;
  }
</style>

<svelte:window on:keydown={handleKeydown} />

<div id="background" class:show={isOpen} on:click={() => (isOpen = false)} />

<div id="modal" class:show={isOpen}>
  <div
    class="w-s24 h-s24 ml-s8 fixed right-s8 top-s8 text-gray-text-alt fill-current"
    on:click={handleClose}
  >
    {@html closeLineIcon}
  </div>
  <slot />
</div>
