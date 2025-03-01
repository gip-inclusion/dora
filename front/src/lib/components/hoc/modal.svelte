<script lang="ts">
  import { browser } from "$app/environment";
  import { closeLineIcon } from "$lib/icons";
  import { createEventDispatcher, onDestroy } from "svelte";
  import Portal from "svelte-portal";
  import "wicg-inert";
  import Button from "../display/button.svelte";

  export let isOpen: boolean;
  export let title: string | undefined = undefined;
  export let subtitle: string | undefined = undefined;
  export let hideTitle = false;
  export let width: "small" | "medium" | undefined = undefined;
  export let noPadding = false;
  export let targetId: string | undefined = undefined;
  export let canClose = true;
  export let hideCloseButton = false;

  const target = (
    targetId ? document.getElementById(targetId) : document.body
  ) as HTMLElement;

  const dispatch = createEventDispatcher();

  const appSelector = "body > div:first-child";

  let activeElementSave: HTMLButtonElement;
  let modalEl: HTMLDivElement;

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
        activeElementSave = document.activeElement as HTMLButtonElement;

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
      role="presentation"
      on:click={handleClose}
      on:keypress={(event) => {
        if (event.code === "Escape") {
          handleClose();
        }
      }}
    >
      <div
        id="modal"
        role="dialog"
        aria-labelledby={title}
        aria-modal="true"
        tabindex="-1"
        bind:this={modalEl}
        class="m-s24 max-h-[90vh] overflow-auto rounded-lg bg-white shadow-md"
        class:px-s36={!noPadding}
        class:py-s24={!noPadding}
        class:w-[560px]={width === "small"}
        class:w-[820px]={width === "medium"}
        class:min-w-[80vw]={!width}
        on:click|stopPropagation
        on:keypress|stopPropagation
      >
        <div class:mb-s24={!hideTitle} class:float-right={hideTitle}>
          <div class="flex justify-between">
            {#if title && !hideTitle}
              <h1
                class="text-f22 text-france-blue md:text-f24 lg:text-f28 xl:text-f32 leading-32 lg:leading-40"
              >
                {title}
              </h1>
            {/if}

            {#if canClose && !hideCloseButton}
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
          {#if subtitle && !hideTitle}
            <div>
              <p class="text-f14 text-gray-text">{subtitle}</p>
            </div>
          {/if}
          {#if $$slots.subtitle && !hideTitle}
            <div class="text-f14 text-gray-text">
              <slot name="subtitle" />
            </div>
          {/if}
          {#if !hideTitle}
            <hr class="-mx-s24 my-s24" />
          {/if}
        </div>

        <div>
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
  @reference "../../../app.css";

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
