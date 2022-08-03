<script>
  export let title;
  export let type = "info";
  import {
    alertLine,
    checkboxCircleLine,
    closeCircleLine,
    informationLine,
  } from "$lib/icons";
  import Button from "./button.svelte";

  import { closeIcon } from "$lib/icons.js";

  export let hasCloseButton = false;
  export let showIcon = true;

  const types = {
    info: {
      bg: "bg-info-light",
      border: "border-info",
      text: "text-info",
      icon: informationLine,
    },
    success: {
      bg: "bg-success-light",
      border: "border-success",
      text: "text-success",
      icon: checkboxCircleLine,
    },
    warning: {
      bg: "bg-warning-light",
      border: "border-warning",
      text: "text-warning",
      icon: alertLine,
    },
    error: {
      bg: "bg-error-light",
      border: "border-error",
      text: "text-error",
      icon: closeCircleLine,
    },
  };

  let visible = true;

  function handleHide() {
    visible = !visible;
  }
</script>

{#if visible}
  <div
    class="rounded-r-md border-l-4 {types[type].border} {types[type]
      .bg} px-s24 pt-s16"
  >
    {#if title || hasCloseButton}
      <div class="flex justify-between">
        {#if title}
          <h4 class="mb-s16 {types[type].text} flex">
            {#if showIcon}
              <div class="mr-s8 h-s24 w-s24 shrink-0 fill-current">
                {@html types[type].icon}
              </div>
            {/if}
            {title}
          </h4>
        {/if}
        {#if hasCloseButton}
          <div class="-mt-s8">
            <Button icon={closeIcon} noBackground on:click={handleHide} small />
          </div>
        {/if}
      </div>
    {/if}
    <div class="flex flex-row flex-wrap items-start justify-between gap-s12">
      <slot />

      {#if $$slots.button}
        <div class="mb-s24 self-end">
          <slot name="button" />
        </div>
      {/if}
    </div>
  </div>
{/if}
