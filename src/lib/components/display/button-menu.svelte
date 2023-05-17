<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import { clickOutside } from "$lib/utils/misc";
  import { randomId } from "$lib/utils/random";

  export let icon: string | undefined = undefined;
  export let label: string | undefined = undefined;
  export let hideLabel = false;
  export let disabled = false;
  export let small = false;

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
    <div
      {id}
      class="right-0 absolute top-[113%] z-[1000] hidden flex-col justify-end rounded-md bg-white shadow-sm"
      class:flex={isOpen}
    >
      <slot onClose={() => (isOpen = false)} />
    </div>
  </div>
</div>
