<script lang="ts">
  export let icon: string;
  export let active: boolean;
  export let label: string;
</script>

<button
  type="button"
  on:click
  class:active
  class="tb-button"
  aria-label={label}
>
  {@html icon}
</button>

<style lang="postcss">
  .tb-button {
    @apply h-s24 w-s24;
  }

  .active {
    @apply bg-gray-02;
  }
</style>
