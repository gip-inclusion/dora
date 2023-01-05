<script lang="ts">
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import { onMount } from "svelte";
  import Button from "./button.svelte";

  export let title = "";
  export let description = "";
  export let noTopPadding = false;
  export let headerBg = "bg-white";
  export let noHeaderBorder = false;
  export let collapsable = false;
  export let collapsed = true;
  export let showModel = false;
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
        : 'border-b border-gray-03 pb-s24'}"
      class:rounded-b-md={collapsed}
    >
      <div class="flex items-center" class:lg:gap-s32={showModel}>
        <div
          class="flex w-full items-center justify-between {showModel
            ? 'lg:w-2/3'
            : ''}"
        >
          <h3
            class={headerBg !== "bg-white" ? "text-white" : "text-france-blue"}
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
        {#if showModel}
          <div class="lg:w-1/3">
            <h5 class="mb-s0 hidden lg:block">Modèle</h5>
          </div>
        {/if}
      </div>
      <slot name="description">
        {#if description}
          <p class="mb-s0 text-f14 text-gray-text-alt2">{description}</p>
        {/if}
      </slot>
    </div>

    {#if $$slots.help && showHelp}
      <div class="border-l-8 border-info bg-info-light  pl-s24 pr-s32  pt-s16">
        <slot name="help" />
      </div>
    {/if}
  {/if}
  <div
    class="flex flex-col gap-s32 bg-white px-s32 pb-s32 pt-s24"
    class:rounded-b-md={title}
    class:rounded-md={!title}
    class:pt-s32={!title}
    class:hidden={collapsable && collapsed}
  >
    <slot />
  </div>
</div>
