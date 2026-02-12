<script lang="ts">
  import type { Component, Snippet } from "svelte";

  import ArrowDownSIcon from "svelte-remix/ArrowDownSLineArrows.svelte";
  import ArrowUpSIcon from "svelte-remix/ArrowUpSLineArrows.svelte";

  import { afterNavigate } from "$app/navigation";

  import { clickOutside } from "$lib/utils/misc";
  import { randomId } from "$lib/utils/random";

  interface Props {
    icon?: Component;
    labelText?: string;
    hideLabel?: boolean;
    withBorders?: boolean;
    withSeparator?: boolean;
    mobileDesign?: boolean;
    label?: Snippet;
    children: Snippet<
      [
        {
          closeDropdown: () => void;
        },
      ]
    >;
    bottom?: Snippet;
  }

  let {
    icon: Icon,
    labelText,
    hideLabel,
    withBorders = false,
    withSeparator = true,
    mobileDesign,
    label,
    children,
    bottom,
  }: Props = $props();

  const id = `dropdown-menu-${randomId()}`;
  let dropdownButton: HTMLButtonElement;

  let isOpen = $state(false);

  function closeDropdown() {
    isOpen = false;
  }

  function onKeyDown(event: KeyboardEvent) {
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
  onkeydown={onKeyDown}
  class="w-full lg:w-auto"
>
  <div class="text-f14 relative flex w-full lg:w-auto">
    <button
      bind:this={dropdownButton}
      aria-expanded={isOpen}
      aria-controls={id}
      class={[
        "flex w-full items-center justify-between rounded-sm text-left lg:w-auto",
        withBorders && "border-gray-03 border",
        isOpen && "bg-magenta-10 border-magenta-cta",
      ]}
      onclick={() => (isOpen = !isOpen)}
    >
      {#if label}
        <div
          class={[
            withBorders && !withSeparator ? "pl-s12" : "px-s12",
            !withBorders && "lg:px-s8",
          ]}
        >
          {@render label()}
        </div>
      {/if}

      <span class="flex items-center" class:pl-s12={!label}>
        {#if Icon}
          <span class="mr-s10 h-s24 w-s24 text-magenta-cta fill-current">
            <Icon />
          </span>
        {/if}

        {#if !label && labelText}
          <span
            class={[
              "text-gray-text text-left whitespace-nowrap",
              hideLabel && "sr-only",
            ]}
          >
            {labelText}
          </span>
        {/if}
      </span>

      <span
        class={[
          "border-gray-03 p-s12 flex",
          !withBorders && "lg:px-s8",
          !!label && withBorders && withSeparator && "border-l",
        ]}
      >
        <span class="h-s24 w-s24 text-magenta-cta fill-current">
          {#if isOpen}
            <ArrowUpSIcon />
          {:else}
            <ArrowDownSIcon />
          {/if}
        </span>
      </span>
    </button>

    <div
      {id}
      class={[
        "border-gray-00 right-s0 absolute top-[100%] z-1000 hidden flex-col justify-end rounded-lg border bg-white shadow-md",
        mobileDesign && "left-s0",
        isOpen && "!flex",
      ]}
    >
      <div class="p-s12 w-full">
        {@render children({ closeDropdown })}
      </div>

      {#if bottom}
        <div class="border-gray-03 px-s24 py-s20 w-full border-t">
          {@render bottom()}
        </div>
      {/if}
    </div>
  </div>
</div>
