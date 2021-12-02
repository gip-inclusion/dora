<script>
  import Label from "$lib/components/label.svelte";
  import { emotionHappyIcon, errorWarningIcon } from "$lib/icons";

  export let label;
  export let positiveMood = false;
  export let negativeMood = false;

  let icon = undefined;
  if (positiveMood || negativeMood) {
    icon = positiveMood ? emotionHappyIcon : errorWarningIcon;
  }
</script>

<style lang="postcss">
  .wrapper {
    padding: var(--s24);
    background-color: var(--col-gray-bg);
  }

  .label-wrapper {
    padding-bottom: var(--s16);
  }

  .details {
    @apply text-gray-text text-f14;
  }
</style>

<div class="wrapper">
  {#if label}
    <div class="label-wrapper">
      <Label
        {label}
        success={positiveMood}
        error={negativeMood}
        {icon}
        bold
        iconOnLeft={!!icon}
      />
    </div>
  {/if}
  <div class="details">
    <slot />
  </div>
</div>
