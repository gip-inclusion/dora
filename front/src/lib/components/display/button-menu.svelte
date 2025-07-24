<script lang="ts">
  import type { Snippet } from "svelte";

  import Button from "$lib/components/display/button.svelte";
  import { clickOutside } from "$lib/utils/misc";
  import { randomId } from "$lib/utils/random";

  interface Props {
    icon?: string | undefined;
    iconOnRight?: boolean;
    label?: string | undefined;
    hideLabel?: boolean;
    disabled?: boolean;
    small?: boolean;
    big?: boolean;
    noPadding?: boolean;
    alignRight?: boolean;
    extraClass?: string;
    children?: Snippet<[any]>;
  }

  let {
    icon = undefined,
    iconOnRight = false,
    label = undefined,
    hideLabel = false,
    disabled = false,
    small = false,
    big = false,
    noPadding = false,
    alignRight = true,
    extraClass = "",
    children,
  }: Props = $props();

  let isOpen = $state(false);
  const id = `button-menu-${randomId()}`;

  function handleClickOutside() {
    isOpen = false;
  }
</script>

<div {@attach clickOutside(handleClickOutside)}>
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
      onclick={() => (isOpen = !isOpen)}
    />
    <div
      {id}
      class="border-gray-01 px-s10 py-s10 absolute top-[113%] z-1000 flex-col justify-end rounded-lg border bg-white shadow-sm"
      class:right-s0={alignRight}
      class:flex={isOpen}
      class:hidden={!isOpen}
    >
      {@render children?.({ onClose: () => (isOpen = false) })}
    </div>
  </div>
</div>
