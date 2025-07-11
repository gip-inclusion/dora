<!-- @migration-task Error while migrating Svelte code: This migration would change the name of a slot (label to label_1) making the component unusable -->
<script lang="ts">
  import { afterNavigate } from "$app/navigation";
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import { clickOutside } from "$lib/utils/misc";
  import { randomId } from "$lib/utils/random";

  export let icon: string | undefined = undefined;
  export let label: string | undefined = undefined;
  export let hideLabel = false;
  export let mobileDesign = false;

  let isOpen = false;
  let dropdownButton;
  const id = `dropdown-menu-${randomId()}`;

  export function closeDropdown() {
    isOpen = false;
  }

  function onKeyDown(event) {
    if (event.key === "Escape") {
      closeDropdown();
      dropdownButton.focus();
    }
  }

  afterNavigate(closeDropdown);
</script>

<div
  {@attach clickOutside(closeDropdown)}
  role="presentation"
  on:keydown={onKeyDown}
  class="w-full lg:w-auto"
>
  <div class="text-f14 relative flex w-full lg:w-auto">
    <button
      bind:this={dropdownButton}
      aria-expanded={isOpen}
      aria-controls={id}
      class:bg-magenta-10={isOpen}
      class="border-gray-03 flex w-full items-center justify-between rounded-sm border text-left lg:w-auto"
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
          <span class="mr-s10 h-s24 w-s24 text-magenta-cta fill-current">
            {@html icon}
          </span>
        {/if}

        {#if !$$slots.label}
          <span
            class:sr-only={hideLabel}
            class="text-gray-text text-left whitespace-nowrap"
          >
            {label}
          </span>
        {/if}
      </span>

      <span class="border-gray-03 p-s12 flex" class:border-l={$$slots.label}>
        <span class="h-s24 w-s24 text-magenta-cta fill-current">
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
      class="border-gray-00 absolute top-[100%] right-0 z-1000 hidden flex-col justify-end rounded-lg border bg-white shadow-md"
      class:left-0={mobileDesign}
      class:!flex={isOpen}
    >
      <div class="p-s12 w-full">
        <slot {closeDropdown} />
      </div>

      {#if $$slots.bottom}
        <div class="border-gray-03 px-s24 py-s20 w-full border-t">
          <slot name="bottom" />
        </div>
      {/if}
    </div>
  </div>
</div>
