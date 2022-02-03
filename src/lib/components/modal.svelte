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
  class="hidden items-center justify-center"
  class:showb={isOpen}
  on:click={handleBackgroundClick}
>
  <div
    class="hidden max-h-screen overflow-y-auto shadow-md"
    class:show={isOpen}
  >
    <div class="md:m-s32" on:click|stopPropagation>
      <div
        class="sticky right-s8 top-s56 ml-auto h-s24 w-s24 fill-current text-gray-text-alt"
        on:click={handleClose}
      >
        {@html closeLineIcon}
      </div>
      <slot />
    </div>
  </div>
</div>

<style lang="postcss">
  #background {
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    display: none;
    width: 100vw;
    height: 100vh;
    background-color: #000000cc;
  }

  .show {
    display: block !important;
  }

  .showb {
    display: flex !important;
  }
</style>
