<script lang="ts">
  import { browser } from "$app/environment";
  import { closeLineIcon } from "$lib/icons";
  import { createEventDispatcher, onDestroy } from "svelte";
  import Portal from "svelte-portal/src/Portal.svelte";
  import "wicg-inert";
  import Button from "../display/button.svelte";

  export let isOpen;
  export let overflow = false;
  export let title: string | undefined = undefined;
  export let subtitle: string | undefined = undefined;
  export let smallWidth = false;
  export let targetId: string | undefined = undefined;
  export let canClose = true;

  const target = (
    targetId ? document.getElementById(targetId) : document.body
  ) as HTMLElement;

  const dispatch = createEventDispatcher();

  const appSelector = "body > div:first-child";

  let activeElementSave;
  let modalEl;

  function closeActions() {
    document.body.style.overflow = "inherit";
    if (modalEl) {
      document.querySelector(appSelector)?.removeAttribute("inert");
    }
    // Retour du focus sur le bouton d'ouverture
    if (activeElementSave) {
      activeElementSave.focus();
    }
  }

  onDestroy(() => closeActions());

  $: {
    // Prevent scrolling the background while the modal is open
    if (browser) {
      if (isOpen) {
        document.body.style.overflow = "hidden";
        // Sauvegarde du bouton à l'origine de la modale
        activeElementSave = document.activeElement;

        setTimeout(() => {
          modalEl.focus();

          // On limite le parcours clavier à la modale en excluant la div immédiatement après le body
          if (!targetId) {
            document.querySelector(appSelector)?.setAttribute("inert", "");
          }
        }, 10);
      } else {
        closeActions();
      }
    }
  }

  function handleClose() {
    if (!canClose) {
      return;
    }

    isOpen = false;
    dispatch("close");
  }
  function handleKeydown(event) {
    if (event.key === "Escape") {
      handleClose();
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if isOpen}
  <Portal {target}>
    <div
      id="background"
      class="flex items-center justify-center"
      on:click={handleClose}
    >
      <div
        id="modal"
        role="dialog"
        aria-labelledby={title}
        aria-modal="true"
        tabindex="-1"
        bind:this={modalEl}
        class="max-h-screen rounded-md bg-white p-s24 shadow-md"
        class:small-width={smallWidth}
        class:min-w-[80vw]={!smallWidth}
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

            {#if canClose}
              <div class="ml-auto">
                <Button
                  icon={closeLineIcon}
                  on:click={handleClose}
                  noBackground
                  noPadding
                  extraClass="-mt-s10"
                />
              </div>
            {/if}
          </div>
          {#if subtitle}
            <div>
              <p class="text-f14 text-gray-text">{subtitle}</p>
            </div>
          {/if}
          <hr class="-mx-s24 my-s24" />
        </div>

        <div class="body max-h-s512 overflow-auto">
          <slot />
        </div>

        {#if $$slots.footer}
          <div class="footer">
            <hr class="-mx-s24 my-s24 mt-s32" />
            <slot name="footer" />
          </div>
        {/if}
      </div>
    </div>
  </Portal>
{/if}

<style lang="postcss">
  .small-width {
    @apply max-w-[560px];
  }

  #background {
    position: fixed;
    z-index: 5000;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: #000000cc;
  }
</style>
