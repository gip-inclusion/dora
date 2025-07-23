<script lang="ts">
  interface Props {
    icon: string;
    active: boolean;
    label: string;
    onclick?: (event: MouseEvent) => void;
  }

  let { icon, active, label, onclick }: Props = $props();
</script>

<button
  type="button"
  {onclick}
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
