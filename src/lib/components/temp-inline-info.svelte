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
  <div class="flex justify-between p-s24 bg-information-light col-span-full">
    <div>
      <div class="mb-s16 text-information text-f17 font-bold">{label}</div>
      <div class="text-gray-text text-f14">{description}</div>
    </div>
    <div class="flex items-baseline">
      <Button label={buttonLabel} on:click={onAction} />
      <Button icon={closeIcon} noBackground on:click={handleHide} />
    </div>
  </div>
{/if}
