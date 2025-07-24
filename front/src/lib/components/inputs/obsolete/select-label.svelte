<script lang="ts">
  import type { Choice } from "$lib/types";

  interface Props {
    choice: Choice;
    showIcon?: boolean;
    useSelectedLabel?: boolean;
  }

  let { choice, showIcon = true, useSelectedLabel = false }: Props = $props();

  let label = $derived(
    useSelectedLabel && choice.selectedLabel
      ? choice.selectedLabel
      : choice.label
  );
</script>

<span
  class="gap-s4 flex w-full items-center"
  class:justify-between={choice.icon && showIcon && choice.iconOnRight}
>
  {#if choice.icon && showIcon && !choice.iconOnRight}
    <span class="mr-s4 h-s24 w-s24 shrink-0 fill-current">
      {@html choice.icon}
    </span>
  {/if}

  {label}

  {#if choice.icon && showIcon && choice.iconOnRight}
    <span class="mr-s4 h-s24 w-s24 shrink-0 fill-current">
      {@html choice.icon}
    </span>
  {/if}
</span>
