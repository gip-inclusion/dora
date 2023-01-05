<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import { clickOutside } from "../../utils/click-outside";

  export let icon = undefined;
  export let label = undefined;
  export let disabled = false;
  export let small = false;
  let isOpen = false;

  function handleClickOutside(_event) {
    isOpen = false;
  }
</script>

<div use:clickOutside on:click_outside={handleClickOutside}>
  <div class="wrapper">
    <Button
      {icon}
      {label}
      noBackground
      {disabled}
      {small}
      on:click={() => (isOpen = !isOpen)}
    />
    <div class="children top-[113%]" class:open={isOpen}>
      <slot onClose={() => (isOpen = false)} />
    </div>
  </div>
</div>

<style lang="postcss">
  .wrapper {
    position: relative;
  }

  .children {
    position: absolute;
    z-index: 1000;
    right: 0;
    display: none;
    flex-direction: column;
    align-items: flex-end;
    padding: var(--s8);
    background-color: var(--col-white);
    border-radius: var(--s8);
    box-shadow: var(--shadow-md);
  }

  .open {
    display: flex;
  }
</style>
