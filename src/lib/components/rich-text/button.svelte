<script>
  export let icon;
  export let active;
</script>

<style lang="postcss">
  .tb-button {
    @apply h-3 w-3;
  }

  .active {
    @apply bg-gray-02;
  }
</style>

<button type="button" on:click class:active class="tb-button">
  {@html icon}
</button>
