<script lang="ts">
  import Label from "$lib/components/display/label.svelte";
  import { emotionHappyIcon, errorWarningIcon } from "$lib/icons";

  interface Props {
    label: any;
    positiveMood?: boolean;
    negativeMood?: boolean;
    info?: boolean;
    icon?: any;
    whiteBg?: boolean;
    leftBorder?: boolean;
    children?: import("svelte").Snippet;
  }

  let {
    label,
    positiveMood = false,
    negativeMood = false,
    info = false,
    icon = $bindable(undefined),
    whiteBg = false,
    leftBorder = false,
    children,
  }: Props = $props();
  if (!icon && (positiveMood || negativeMood)) {
    icon = positiveMood ? emotionHappyIcon : errorWarningIcon;
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
