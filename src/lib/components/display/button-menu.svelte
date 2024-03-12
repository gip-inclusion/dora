<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import { clickOutside } from "$lib/utils/misc";
  import { randomId } from "$lib/utils/random";

  export let icon: string | undefined = undefined;
  export let iconOnRight = false;
  export let label: string | undefined = undefined;
  export let hideLabel = false;
  export let disabled = false;
  export let small = false;
  export let big = false;
  export let noPadding = false;
  export let alignRight = true;
  export let extraClass = "";

  let isOpen = false;
  const id = `button-menu-${randomId()}`;

  function handleClickOutside(_event) {
    isOpen = false;
  }
</script>

<div use:clickOutside on:click_outside={handleClickOutside}>
  <div class="wrapper relative">
    <Button
      {icon}
      {iconOnRight}
      {label}
      noBackground
      {hideLabel}
      ariaAttributes={{
        "aria-expanded": isOpen,
        "aria-controls": id,
      }}
      {extraClass}
      {disabled}
      {small}
      {big}
      {noPadding}
      on:click={() => (isOpen = !isOpen)}
    />
    <div
      {id}
      class="absolute top-[113%] z-[1000] flex-col justify-end rounded-md border border-gray-01 bg-white px-s10 py-s10 shadow-sm"
      class:right-s0={alignRight}
      class:flex={isOpen}
      class:hidden={!isOpen}
    >
      <slot onClose={() => (isOpen = false)} />
    </div>
  </div>
</div>
