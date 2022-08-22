<script lang="ts">
  import { browser } from "$app/env";
  import { closeLineIcon } from "$lib/icons";
  import Button from "./button.svelte";
  import { createEventDispatcher } from "svelte";

  export let isOpen;
  export let overflow = false;
  export let title: string | undefined = undefined;
  export let subtitle: string | undefined = undefined;

  const dispatch = createEventDispatcher();

  $: {
    // Prevent scrolling the background while the modal is open
    if (browser) {
      document.body.style.overflow = isOpen ? "hidden" : "visible";
    }
  }

  function handleClose() {
    isOpen = false;
    dispatch("close");
  }
  function handleKeydown(event) {
    if (event.key === "Escape") handleClose();
  }
</script>

<svelte:window on:keydown={handleKeydown} />

<div
  id="background"
  class="flex items-center justify-center"
  class:hidden={!isOpen}
  on:click={handleClose}
>
  <div
    class="max-h-screen min-w-[80vw] overflow-auto rounded-md bg-white p-s24 shadow-md"
    class:overflow-y-auto={overflow}
    on:click|stopPropagation
  >
    <div class="mb-s24 border border-l-0 border-r-0 border-t-0 border-gray-02">
      <div class="flex justify-between">
        {#if title}
          <h1
            class="text-f22 leading-32 text-france-blue md:text-f24 lg:text-f28 lg:leading-40 xl:text-f32"
          >
            {title}
          </h1>
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
      {#if subtitle}
        <div>
          <p class="text-f14 text-gray-text">{subtitle}</p>
        </div>
      {/if}
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
