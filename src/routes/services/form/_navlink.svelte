<script>
  export let name;
  export let active;
  export let lit;
</script>

<button
  class="text-center text-f16 text-gray-text-alt2 border-b-2 border-gray-02 px-s16 py-0"
  type="button"
  href=""
  on:click
  class:active
  disabled={!lit}
>
  {name}
</button>

<style lang="postcss">
  .active {
    @apply border-b-4 border-magenta-brand text-magenta-cta;
  }
</style>
