<script lang="ts">
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import { onMount } from "svelte";
  import Button from "./button.svelte";
  import { randomId } from "$lib/utils/random";

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
    const breakPoint = window
      .getComputedStyle(wrapper, ":before")
      .content.replace(/"/gu, "");

    collapsed = breakPoint === "xs" || breakPoint === "md";
  });

  function toggleFold() {
    collapsed = !collapsed;
  }

  let showHelp = false;
  const helpId = randomId();

  function toggleHelp() {
    showHelp = !showHelp;
  }
</script>

<fieldset
  class="breakpoint-hack flex flex-col rounded-lg shadow-md"
  class:mt-s48={!noTopPadding}
  bind:this={wrapper}
>
  {#if title}
    <div
      class="px-s32 pt-s32 rounded-t-md {headerBg} {noHeaderBorder
        ? ''
        : 'border-gray-03 pb-s24 border-b'}"
      class:rounded-b-md={collapsed}
    >
      <div class="flex items-center" class:lg:gap-s32={showModel}>
        <div
          class="flex w-full items-center justify-between {showModel
            ? 'lg:w-2/3'
            : ''}"
        >
          <h2
            class={`text-f21 leading-32 ${headerBg !== "bg-white" ? "text-white" : "text-france-blue"}`}
          >
            {title}
          </h2>
          <div class="flex">
            {#if $$slots.help}
              <Button
                ariaAttributes={{
                  "aria-expanded": showHelp,
                  "aria-controls": helpId,
                }}
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
      <div
        id={helpId}
        class="border-info bg-info-light py-s16 pl-s24 pr-s32 border-l-8"
      >
        <slot name="help" />
      </div>
    {/if}
  {/if}
  <div
    class="gap-s32 px-s32 pb-s32 pt-s24 flex flex-col bg-white"
    class:rounded-b-md={title}
    class:rounded-lg={!title}
    class:pt-s32={!title}
    class:hidden={collapsable && collapsed}
  >
    <slot />
  </div>
</fieldset>
