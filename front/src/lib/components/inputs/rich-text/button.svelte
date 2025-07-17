<script lang="ts">
  import { createBubbler } from "svelte/legacy";

  const bubble = createBubbler();
  interface Props {
    icon: string;
    active: boolean;
    label: string;
  }

  let { icon, active, label }: Props = $props();
</script>

<button
  type="button"
  onclick={bubble("click")}
  class:active
  class="tb-button"
  aria-label={label}
>
  {@html icon}
</button>

<style lang="postcss">
  @reference "../../../../app.css";

  .tb-button {
    @apply h-s24 w-s24;
  }

  .active {
    @apply bg-gray-02;
  }
</style>
