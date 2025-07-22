<!-- @migration-task Error while migrating Svelte code: This migration would change the name of a slot (description to description_1) making the component unusable -->
<script lang="ts">
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import { onMount, type Snippet } from "svelte";
  import Button from "./button.svelte";
  import { randomId } from "$lib/utils/random";

  interface Props {
    title?: string;
    noTopPadding?: boolean;
    headerBg?: string;
    noHeaderBorder?: boolean;
    collapsable?: boolean;
    collapsed?: boolean;
    showModel?: boolean;
    descriptionText?: string;
    description?: Snippet;
    help?: Snippet;
    children?: Snippet;
  }

  let {
    title = "",
    noTopPadding = false,
    headerBg = "bg-white",
    noHeaderBorder = false,
    collapsable = false,
    collapsed = true,
    showModel = false,
    descriptionText,
    description,
    help,
    children,
  }: Props = $props();

  let wrapper: HTMLElement;
  let showHelp = $state(false);
  const helpId = randomId();

  onMount(() => {
    if (wrapper) {
      const breakPoint = window
        .getComputedStyle(wrapper, ":before")
        .content.replace(/"/gu, "");

      collapsed = breakPoint === "xs" || breakPoint === "md";
    }
  });

  function toggleFold() {
    collapsed = !collapsed;
  }

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
            {#if help}
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
      {#if description}
        {@render description()}
      {:else if descriptionText}
        <p class="mb-s0 text-f14 text-gray-text-alt2">{descriptionText}</p>
      {/if}
    </div>

    {#if help && showHelp}
      <div
        id={helpId}
        class="border-info bg-info-light py-s16 pl-s24 pr-s32 border-l-8"
      >
        {@render help()}
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
    {@render children?.()}
  </div>
</fieldset>
