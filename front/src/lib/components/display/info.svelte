<script lang="ts">
  import type { Component, Snippet } from "svelte";

  import EmotionHappyFillUserFaces from "svelte-remix/EmotionHappyFillUserFaces.svelte";
  import ErrorWarningFillSystem from "svelte-remix/ErrorWarningFillSystem.svelte";

  import Label from "$lib/components/display/label.svelte";

  interface Props {
    label?: string;
    positiveMood?: boolean;
    negativeMood?: boolean;
    info?: boolean;
    icon?: Component;
    whiteBg?: boolean;
    leftBorder?: boolean;
    children?: Snippet;
  }

  let {
    label,
    positiveMood = false,
    negativeMood = false,
    info = false,
    icon = $bindable(),
    whiteBg = false,
    leftBorder = false,
    children,
  }: Props = $props();

  if (!icon && (positiveMood || negativeMood)) {
    icon = positiveMood ? EmotionHappyFillUserFaces : ErrorWarningFillSystem;
  }
</script>

<div
  class="bg-gray-bg p-s24"
  class:bg-white={whiteBg}
  class:border-l-4={leftBorder}
  class:border-info={leftBorder}
>
  {#if label}
    <div class="pb-s16">
      <Label
        {label}
        success={positiveMood}
        error={negativeMood}
        {info}
        {icon}
        bold
      />
    </div>
  {/if}
  <div class="text-f14 text-gray-text">
    {@render children?.()}
  </div>
</div>
