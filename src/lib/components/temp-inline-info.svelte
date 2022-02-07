<script>
  import Button from "./button.svelte";
  import { closeIcon } from "$lib/icons.js";

  export let label;
  export let description;
  export let buttonLabel;
  export let onAction;
  export let onHide;
  let visible = true;

  function handleHide() {
    if (onHide) {
      onHide();
    } else {
      visible = false;
    }
  }
</script>

{#if visible}
  <div class="col-span-full flex justify-between bg-information-light p-s24">
    <div>
      <div class="mb-s16 text-f17 font-bold text-information">{label}</div>
      <div class="text-f14 text-gray-text">{description}</div>
    </div>
    <div class="flex items-baseline">
      <Button label={buttonLabel} on:click={onAction} />
      <Button icon={closeIcon} noBackground on:click={handleHide} />
    </div>
  </div>
{/if}
