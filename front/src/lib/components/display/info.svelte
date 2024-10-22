<script lang="ts">
  import Label from "$lib/components/display/label.svelte";
  import { emotionHappyIcon, errorWarningIcon } from "$lib/icons";

  export let label;
  export let positiveMood = false;
  export let negativeMood = false;
  export let info = false;
  export let icon = undefined;
  export let whiteBg = false;
  export let leftBorder = false;
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
    <slot />
  </div>
</div>
