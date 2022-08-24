<script lang="ts">
  import { browser } from "$app/env";
  import { closeLineIcon } from "$lib/icons";
  import Button from "./button.svelte";
  import { createEventDispatcher } from "svelte";

  export let isOpen;
  export let overflow = false;
  export let title: string | undefined = undefined;
  export let subtitle: string | undefined = undefined;
  export let smallWidth = false;

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

{#if isOpen}
  <div
    id="background"
    class="flex items-center justify-center"
    on:click={handleClose}
  >
    <div
      class="max-h-screen min-w-[80vw] rounded-md bg-white p-s24 shadow-md"
      class:small-width={smallWidth}
      class:overflow-y-auto={overflow}
      on:click|stopPropagation
    >
      <div class="mb-s24">
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
              noPadding
              extraClass="-mt-s10"
            />
          </div>
        </div>
        {#if subtitle}
          <div>
            <p class="text-f14 text-gray-text">{subtitle}</p>
          </div>
        {/if}
        <hr class="my-s24 -mx-s24" />
      </div>

      <div class="body max-h-s512 overflow-auto">
        <slot />
      </div>

      {#if $$slots.footer}
        <div class="footer">
          <hr class="my-s24 -mx-s24 mt-s32" />
          <slot name="footer" />
        </div>
      {/if}
    </div>
  </div>
{/if}

<style lang="postcss">
  .small-width {
    @apply min-w-[560px];
  }

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
