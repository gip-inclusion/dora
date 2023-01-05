<script lang="ts">
  export let icon;
  export let active;
</script>

<button type="button" on:click class:active class="tb-button">
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
