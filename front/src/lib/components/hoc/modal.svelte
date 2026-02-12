<script lang="ts">
  import type { Snippet } from "svelte";
  import { onDestroy } from "svelte";

  import Portal from "svelte-portal";

  import CloseLineSystem from "svelte-remix/CloseLineSystem.svelte";

  import "wicg-inert";

  import { browser } from "$app/environment";

  import Button from "../display/button.svelte";

  interface Props {
    isOpen: boolean;
    title?: string;
    subtitleText?: string;
    hideTitle?: boolean;
    width?: "small" | "medium";
    noPadding?: boolean;
    targetId?: string;
    canClose?: boolean;
    hideCloseButton?: boolean;
    onClose?: () => void;
    subtitle?: Snippet;
    children?: Snippet;
    footer?: Snippet;
    hideOverflow?: boolean;
  }

  let {
    isOpen = $bindable(),
    title = undefined,
    subtitleText = undefined,
    hideTitle = false,
    width = undefined,
    noPadding = false,
    targetId = undefined,
    canClose = true,
    hideCloseButton = false,
    onClose = undefined,
    subtitle = undefined,
    children = undefined,
    footer = undefined,
    hideOverflow = false,
  }: Props = $props();

  const target = (
    targetId ? document.getElementById(targetId) : document.body
  ) as HTMLElement;

  const appSelector = "body > div:first-child";

  let activeElementSave = $state<HTMLButtonElement | null>(null);
  let modalEl = $state<HTMLDivElement | null>(null);

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

  $effect(() => {
    let timeout: ReturnType<typeof setTimeout>;
    // Prevent scrolling the background while the modal is open
    if (browser) {
      if (isOpen) {
        document.body.style.overflow = "hidden";
        // Sauvegarde du bouton à l'origine de la modale
        activeElementSave = document.activeElement as HTMLButtonElement;

        timeout = setTimeout(() => {
          if (modalEl) {
            modalEl.focus();

            // On limite le parcours clavier à la modale en excluant la div immédiatement après le body
            if (!targetId) {
              document.querySelector(appSelector)?.setAttribute("inert", "");
            }
          }
        }, 10);
      } else {
        closeActions();
      }
    }
    return () => timeout && clearTimeout(timeout);
  });

  function handleClose() {
    if (!canClose) {
      return;
    }

    isOpen = false;
    onClose?.();
  }

  function handleKeydown(event) {
    if (event.key === "Escape") {
      handleClose();
    }
  }

  function handleModalClick(event) {
    event.stopPropagation();
  }

  function handleModalKeypress(event) {
    event.stopPropagation();
  }
</script>

<svelte:window onkeydown={handleKeydown} />

{#if isOpen}
  <Portal {target}>
    <div
      id="background"
      class="flex items-center justify-center"
      role="presentation"
      onclick={handleClose}
      onkeypress={(event) => {
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
        class="m-s24 max-h-[90vh] rounded-lg bg-white shadow-md"
        class:px-s36={!noPadding}
        class:py-s24={!noPadding}
        class:w-[560px]={width === "small"}
        class:w-[820px]={width === "medium"}
        class:min-w-[80vw]={!width}
        class:overflow-auto={!hideOverflow}
        class:overflow={hideOverflow}
        onclick={handleModalClick}
        onkeypress={handleModalKeypress}
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
                  icon={CloseLineSystem}
                  onclick={handleClose}
                  noBackground
                  noPadding
                  extraClass="-mt-s10"
                />
              </div>
            {/if}
          </div>
          {#if subtitleText && !hideTitle}
            <div>
              <p class="text-f14 text-gray-text">{subtitleText}</p>
            </div>
          {/if}
          {#if subtitle && !hideTitle}
            <div class="text-f14 text-gray-text">
              {@render subtitle()}
            </div>
          {/if}
          {#if !hideTitle}
            <hr class="-mx-s24 my-s24" />
          {/if}
        </div>

        {#if children}
          <div>
            {@render children()}
          </div>
        {/if}

        {#if footer}
          <div class="footer">
            <hr class="-mx-s24 my-s24 mt-s32" />
            {@render footer()}
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
    width: 100%;
    height: 100%;
    background-color: #000000cc;
  }
</style>
