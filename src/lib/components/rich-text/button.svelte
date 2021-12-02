<script>
  export let icon;
  export let active;
</script>

<style lang="postcss">
  .tb-button {
    @apply h-s24 w-s24;
  }

  .active {
    @apply bg-gray-02;
  }
</style>

<button type="button" on:click class:active class="tb-button">
  {@html icon}
</button>
