<script>
  import { onMount } from "svelte";
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import Button from "../button.svelte";

  export let title = "";
  export let description = "";
  export let noTopPadding = false;
  export let headerBg = "bg-white";
  export let noHeaderBorder = false;
  export let collapsable = false;
  export let collapsed = true;
  export let noSpacing = false;
  let wrapper;

  onMount(() => {
    const bp = window
      .getComputedStyle(wrapper, ":before")
      .content.replace(/"/gu, "");

    collapsed = bp === "xs" || bp === "md";
  });

  function toggleFold() {
    collapsed = !collapsed;
  }

  let showHelp = false;

  function toggleHelp() {
    showHelp = !showHelp;
  }
</script>

<div
  class="breakpoint-hack flex flex-col rounded-md shadow-md"
  class:mt-s48={!noTopPadding}
  bind:this={wrapper}
>
  {#if title}
    <div
      class="rounded-t-md px-s32 pt-s32 {headerBg} {noHeaderBorder
        ? ''
        : 'border-b border-gray-01 pb-s24'}"
    >
      <div class="flex justify-between">
        <h3
          class="mb-s0 {headerBg !== 'bg-white'
            ? 'text-white'
            : 'text-france-blue'}"
        >
          {title}
        </h3>
        <div class="flex">
          {#if $$slots.help}
            <Button
              label="Aide"
              on:click={toggleHelp}
              icon={!showHelp ? arrowDownSIcon : arrowUpSIcon}
              iconOnRight
              noBackground
              small
            />
          {/if}

          {#if collapsable}
            <Button
              on:click={toggleFold}
              icon={collapsed ? arrowDownSIcon : arrowUpSIcon}
              noBackground
              small
            />
          {/if}
        </div>
      </div>
      <slot name="description">
        {#if description}
          <p class="mb-s0 text-f14 text-gray-text-alt2">{description}</p>
        {/if}
      </slot>
    </div>
  {/if}

  {#if $$slots.help && showHelp}
    <div class="border-l-8 border-info bg-info-light  pl-s24 pr-s32  pt-s16">
      <slot name="help" />
    </div>
  {/if}
  <div
    class="rounded-b-md bg-white px-s32 pb-s32 pt-s24"
    class:pt-s32={!title}
    class:hidden={collapsable && collapsed}
    class:flex={!noSpacing}
    class:flex-col={!noSpacing}
    class:gap-s24={!noSpacing}
  >
    <slot />
  </div>
</div>
