<script lang="ts">
  import { afterNavigate } from "$app/navigation";
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import { clickOutside } from "$lib/utils/misc";
  import { randomId } from "$lib/utils/random";

  export let icon: string | undefined = undefined;
  export let label: string | undefined = undefined;
  export let hideLabel = false;
  export let mobileDesign = false;
  export let minWidth: string | undefined = undefined;

  let isOpen = false;
  let dropdownButton;
  const id = `dropdown-menu-${randomId()}`;

  function handleClickOutside(_event) {
    isOpen = false;
  }
  function onKeyDown(event) {
    if (event.key === "Escape") {
      isOpen = false;
      dropdownButton.focus();
    }
  }

  afterNavigate(() => {
    isOpen = false;
  });
</script>

<div
  use:clickOutside
  on:click_outside={handleClickOutside}
  on:keydown={onKeyDown}
  class="w-full lg:w-auto"
>
  <div class="relative flex w-full text-f14 lg:w-auto">
    <button
      bind:this={dropdownButton}
      aria-expanded={isOpen}
      aria-controls={id}
      class:bg-magenta-10={isOpen}
      class="flex w-full items-center justify-between rounded border border-gray-03 text-left lg:w-auto"
      class:border-magenta-cta={isOpen}
      on:click={() => (isOpen = !isOpen)}
    >
      {#if $$slots.label}
        <div class="px-s12">
          <slot name="label" />
        </div>
      {/if}

      <span class="flex items-center" class:pl-s12={!$$slots.label}>
        {#if icon}
          <span class="mr-s10 h-s24 w-s24 fill-current text-magenta-cta">
            {@html icon}
          </span>
        {/if}

        {#if !$$slots.label}
          <span
            class:sr-only={hideLabel}
            class="whitespace-nowrap text-left text-gray-text"
          >
            {label}
          </span>
        {/if}
      </span>

      <span class="flex border-gray-03 p-s12" class:border-l={$$slots.label}>
        <span class="h-s24 w-s24 fill-current text-magenta-cta">
          {#if isOpen}
            {@html arrowUpSIcon}
          {:else}
            {@html arrowDownSIcon}
          {/if}
        </span>
      </span>
    </button>

    <div
      {id}
      class="
        right-0 absolute top-[100%] z-[1000] hidden flex-col justify-end rounded-md border border-gray-00 bg-white shadow-md
        {minWidth ? `min-w-[${minWidth}]` : ''}
        "
      class:left-0={mobileDesign}
      class:!flex={isOpen}
    >
      <div class="w-full p-s12">
        <slot />
      </div>

      {#if $$slots.bottom}
        <div class="w-full border-t border-gray-03 px-s24 py-s20">
          <slot name="bottom" />
        </div>
      {/if}
    </div>
  </div>
</div>
