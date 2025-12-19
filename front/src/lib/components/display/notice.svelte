<script lang="ts">
  import type { Snippet } from "svelte";

  import InformationFillSystem from "svelte-remix/InformationFillSystem.svelte";
  import ErrorWarningFillSystem from "svelte-remix/ErrorWarningFillSystem.svelte";
  import CloseCircleFillSystem from "svelte-remix/CloseCircleFillSystem.svelte";
  import CheckboxCircleFillSystem from "svelte-remix/CheckboxCircleFillSystem.svelte";
  import CloseFillSystem from "svelte-remix/CloseFillSystem.svelte";

  interface Props {
    title?: string;
    type?: "info" | "success" | "warning" | "error";
    hasCloseButton?: boolean;
    showIcon?: boolean;
    titleLevel?: "h2" | "h3" | "h4";
    children?: Snippet;
    button?: Snippet;
  }

  let {
    title = "",
    type = "info",
    hasCloseButton = false,
    showIcon = true,
    titleLevel = "h4",
    children,
    button,
  }: Props = $props();

  const types = {
    info: {
      background: "bg-info-light",
      text: "text-info",
      title: "text-france-blue",
      icon: InformationFillSystem,
    },
    success: {
      background: "bg-success-light",
      text: "text-success",
      title: "text-success",
      icon: CheckboxCircleFillSystem,
    },
    warning: {
      background: "bg-warning-light",
      text: "text-warning",
      title: "text-warning",
      icon: ErrorWarningFillSystem,
    },
    error: {
      background: "bg-error-light",
      text: "text-error",
      title: "text-error",
      icon: CloseCircleFillSystem,
    },
  };

  let visible = $state(true);

  function handleHide() {
    visible = !visible;
  }
</script>

{#if visible}
  <section
    class="py-s32 px-s16 gap-s16 flex flex-col rounded-2xl sm:flex-row {types[
      type
    ].background}"
  >
    {#if showIcon}
      {@const SvelteComponent = types[type].icon}
      <div class={types[type].text}>
        <SvelteComponent size={32} />
      </div>
    {/if}

    <div class="gap-s8 flex flex-col">
      {#if title || hasCloseButton}
        <div
          class="flex flex-row items-center justify-between {types[type].title}"
        >
          {#if title}
            <svelte:element
              this={titleLevel}
              class="text-f18 mb-s0 leading-24 {types[type].title}"
            >
              {title}
            </svelte:element>
          {/if}
          {#if hasCloseButton}
            <button onclick={handleHide}>
              <CloseFillSystem size={24} />
            </button>
          {/if}
        </div>
      {/if}

      {#if children || button}
        <div
          class="gap-s12 text-gray-dark flex flex-row flex-wrap items-start justify-between"
        >
          {@render children?.()}

          {#if button}
            <div class="mb-s0 self-end">
              {@render button?.()}
            </div>
          {/if}
        </div>
      {/if}
    </div>
  </section>
{/if}
