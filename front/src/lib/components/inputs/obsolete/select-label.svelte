<script lang="ts">
  import { run } from 'svelte/legacy';

  import type { Choice } from "$lib/types";

  interface Props {
    choice: Choice;
    showIcon?: boolean;
    useSelectedLabel?: boolean;
  }

  let { choice, showIcon = true, useSelectedLabel = false }: Props = $props();

  let icon = $state(), iconOnRight = $state(), label = $state();
  run(() => {
    icon = choice.icon;
    iconOnRight = choice.iconOnRight;
    label =
      useSelectedLabel && choice.selectedLabel
        ? choice.selectedLabel
        : choice.label;
  });
</script>

<span
  class="gap-s4 flex w-full items-center"
  class:justify-between={icon && showIcon && iconOnRight}
>
  {#if icon && showIcon && !iconOnRight}
    <span class="mr-s4 h-s24 w-s24 shrink-0 fill-current">
      {@html icon}
    </span>
  {/if}

  {label}

  {#if icon && showIcon && iconOnRight}
    <span class="mr-s4 h-s24 w-s24 shrink-0 fill-current">
      {@html icon}
    </span>
  {/if}
</span>
