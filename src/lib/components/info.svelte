<script>
  import Label from "$lib/components/label.svelte";
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

<div class="wrapper" class:white-bg={whiteBg} class:left-border={leftBorder}>
  {#if label}
    <div class="label-wrapper">
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
  <div class="details">
    <slot />
  </div>
</div>

<style lang="postcss">
  .wrapper {
    padding: var(--s24);
    background-color: var(--col-gray-bg);
  }

  .white-bg {
    background-color: var(--col-white);
  }

  .label-wrapper {
    padding-bottom: var(--s16);
  }

  .details {
    @apply text-f14 text-gray-text;
  }

  .left-border {
    @apply border-l-4 border-information;
  }
</style>
