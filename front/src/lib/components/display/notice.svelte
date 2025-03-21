<script lang="ts">
  import {
    alertLine,
    checkboxCircleFillIcon,
    closeCircleIcon,
    closeIcon,
    informationLineIcon,
  } from "$lib/icons";
  import Button from "./button.svelte";

  export let title = "";
  export let type: "info" | "success" | "warning" | "error" = "info";
  export let hasCloseButton = false;
  export let showIcon = true;
  export let titleLevel: "h2" | "h3" | "h4" = "h4";

  const types = {
    info: {
      background: "bg-info-light",
      text: "text-info",
      title: "text-info",
      icon: informationLineIcon,
    },
    success: {
      background: "bg-success-light",
      text: "text-success",
      title: "text-success",
      icon: checkboxCircleFillIcon,
    },
    warning: {
      background: "bg-warning-light",
      text: "text-warning",
      title: "text-warning",
      icon: alertLine,
    },
    "warning-dark": {
      background: "bg-warning-dark",
      text: "text-warning",
      title: "text-warning",
      icon: alertLine,
    },
    error: {
      background: "bg-error-light",
      text: "text-error",
      title: "text-error",
      icon: closeCircleIcon,
    },
  };

  let visible = true;

  function handleHide() {
    visible = !visible;
  }
</script>

{#if visible}
  <div class="rounded-3xl {types[type].background} py-s24 pl-s24 pr-s24">
    {#if title || hasCloseButton}
      <div class="items-top flex">
        {#if showIcon}
          <div class="hidden flex-[0_0_48px] text-center sm:block">
            <div class="{types[type].text} h-s32 w-s32 shrink-0 fill-current">
              {@html types[type].icon}
            </div>
          </div>
        {/if}

        {#if title}
          <svelte:element
            this={titleLevel}
            class="mb-s0 text-f18 flex leading-32 {types[type].title}"
          >
            {#if showIcon}
              <div class="mr-s8 inline-block text-center sm:hidden">
                <div
                  class="{types[type]
                    .text} h-s32 w-s32 m-auto shrink-0 fill-current"
                >
                  {@html types[type].icon}
                </div>
              </div>
            {/if}

            {title}
          </svelte:element>
        {/if}
        {#if hasCloseButton}
          <div>
            <Button icon={closeIcon} noBackground on:click={handleHide} small />
          </div>
        {/if}
      </div>
    {/if}
    {#if $$slots?.default || $$slots.button}
      <div
        class="gap-s12 flex flex-row flex-wrap items-start justify-between"
        class:mt-s16={!!title}
        class:mt-s8={!title}
      >
        <slot />

        {#if $$slots.button}
          <div class="mb-s0 self-end">
            <slot name="button" />
          </div>
        {/if}
      </div>
    {/if}
  </div>
{/if}
