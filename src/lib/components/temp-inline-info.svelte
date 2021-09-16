<script>
  import Button from "./button.svelte";
  import { closeIcon } from "$lib/icons.js";

  export let label;
  export let description;
  export let buttonLabel;
  export let onAction;
  let visible = true;
</script>

<style>
  .wrapper {
    display: flex;
    justify-content: space-between;
    padding: var(--s24);
    background: var(--col-info-light);
    grid-column: 1/-1;
  }

  .label {
    margin-bottom: var(--s16);
    color: var(--col-info);
    font-size: var(--f17);
    font-weight: bold;
  }

  .description {
    color: var(--col-text);
    font-size: var(--f14);
  }

  .buttons {
    display: flex;
  }
</style>

{#if visible}
  <div class="wrapper">
    <div>
      <div class="label">{label}</div>
      <div class="description">{description}</div>
    </div>
    <div class="buttons">
      <Button label={buttonLabel} on:click={onAction} />
      <Button
        icon={closeIcon}
        noBackground
        on:click={() => (visible = false)} />
    </div>
  </div>
{/if}
