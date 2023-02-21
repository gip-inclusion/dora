<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import { clickOutside } from "$lib/utils/misc";

  export let icon: string | undefined = undefined;
  export let label: string | undefined = undefined;
  export let hideLabel = false;
  export let disabled = false;
  export let small = false;

  let isOpen = false;
  const id = `button-menu-${crypto.randomUUID()}`;

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
      {hideLabel}
      ariaAttributes={{
        "aria-expanded": isOpen,
        "aria-controls": id,
      }}
      {disabled}
      {small}
      on:click={() => (isOpen = !isOpen)}
    />
    <div {id} class="children top-[113%]" class:open={isOpen}>
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
