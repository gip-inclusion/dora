<script>
  import Label from "$lib/components/label.svelte";
  import { emotionHappyIcon, errorWarningIcon } from "$lib/icons";

  export let label;
  export let positiveMood = false;
  export let negativeMood = false;

  const icon = positiveMood ? emotionHappyIcon : errorWarningIcon;
</script>

<style>
  .wrapper {
    padding: var(--s24);
  }

  .positive {
    background-color: #deedea;
  }

  .negative {
    background-color: #fbe4e5;
  }

  .details {
    padding-left: var(--s32);
    color: var(--col-text);
    font-size: var(--f14);
  }
</style>

<div
  class="wrapper"
  class:positive={positiveMood}
  class:negative={negativeMood}
>
  <Label
    {label}
    success={positiveMood}
    error={negativeMood}
    {icon}
    bold
    iconOnLeft
  />
  <div class="details">
    <slot name="details" />
  </div>
</div>
