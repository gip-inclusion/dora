<script>
  // https://tailwindcomponents.com/component/toggle-button-1

  export let checked = undefined;
</script>

<style lang="postcss">
  .toggle-path {
    transition: all 0.15s ease-in-out;
  }
  .toggle-circle {
    transition: all 0.15s ease-in-out;
    top: 0.25rem;
    left: 0.25rem;
  }
  input:checked ~ .toggle-circle {
    transform: translateX(100%);
    @apply bg-dora-magenta-cta;
  }
  input:checked ~ .toggle-path {
    @apply border-dora-magenta-hover bg-magenta-20;
  }
</style>

<div class="relative flex flex-row">
  <input type="checkbox" bind:checked class="hidden" />
  <!-- path -->
  <div
    class="w-5 h-3 bg-white border rounded-full toggle-path border-gray-03" />
  <!-- circle -->
  <div
    class="absolute inset-y-0 left-0 w-2 h-2 rounded-full bg-gray-03 toggle-circle" />
</div>
