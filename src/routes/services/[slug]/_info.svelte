<script>
  import Label from "$lib/components/label.svelte";
  import { emotionHappyIcon, errorWarningIcon } from "$lib/icons";

  export let label;
  export let positiveMood = false;
  export let negativeMood = false;

  const icon = positiveMood ? emotionHappyIcon : errorWarningIcon;
</script>

<div
  class="wrapper"
  class:positive={positiveMood}
  class:negative={negativeMood}
>
  <Label {label} success={positiveMood} error={negativeMood} {icon} bold />
  <div class=" pl-s32 text-f14 text-gray-text">
    <slot name="details" />
  </div>
</div>

<style lang="postcss">
  .wrapper {
    padding: var(--s24);
  }

  .positive {
    background-color: #deedea;
  }

  .negative {
    background-color: #fbe4e5;
  }
</style>
