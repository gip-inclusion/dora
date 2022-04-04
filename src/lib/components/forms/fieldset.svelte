<script>
  import { onMount } from "svelte";
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";

  export let title = "";
  export let description = "";
  export let noTopPadding = false;
  export let headerBg = "bg-white";
  export let noHeaderBorder = false;
  export let collapsable = false;
  export let collapsed = true;
  let wrapper;

  onMount(() => {
    const bp = window
      .getComputedStyle(wrapper, ":before")
      .content.replace(/"/gu, "");

    collapsed = bp === "xs" || bp === "md";
  });

  function handleToggleFold() {
    collapsed = !collapsed;
  }
</script>

<div
  class="breakpoint-hack flex flex-col rounded-md shadow-md"
  class:mt-s48={!noTopPadding}
  bind:this={wrapper}
>
  {#if title}
    <div
      class="rounded-t-md px-s40 pt-s32 {headerBg} {noHeaderBorder
        ? ''
        : 'border-b border-gray-01 pb-s24'}"
    >
      <div class="flex justify-between">
        <h3
          class="mb-s8 {headerBg !== 'bg-white'
            ? 'text-white'
            : 'text-france-blue'}"
        >
          {title}
        </h3>
        {#if collapsable}
          <div
            class="ml-s8 h-s24 w-s24 fill-current text-magenta-cta"
            on:click={handleToggleFold}
          >
            {@html collapsed ? arrowDownSIcon : arrowUpSIcon}
          </div>
        {/if}
      </div>
      <slot name="description">
        {#if description}
          <p class="text-f14 text-gray-text-alt2">{description}</p>
        {/if}
      </slot>
    </div>
  {/if}
  <div
    class="flex flex-col gap-s24 rounded-b-md bg-white px-s40 pb-s40 pt-s24"
    class:pt-s32={!title}
    class:hidden={collapsable && collapsed}
  >
    <slot />
  </div>
</div>
