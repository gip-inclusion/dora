<script lang="ts">
  import type { Choice } from "$lib/types";

  export let choice: Choice;
  export let showIcon = true;
  export let useSelectedLabel = false;

  let icon, iconOnRight, label;
  $: {
    icon = choice.icon;
    iconOnRight = choice.iconOnRight;
    label =
      useSelectedLabel && choice.selectedLabel
        ? choice.selectedLabel
        : choice.label;
  }
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
