<script>
  // https://tailwindcomponents.com/component/toggle-button-1

  export let checked;
</script>

<style>
  .toggle-path {
    transition: background 0.3s ease-in-out;
  }
  .toggle-circle {
    top: 0.1rem;
    left: 0.15rem;
    transition: all 0.3s ease-in-out;
  }
  input:checked ~ .toggle-circle {
    transform: translateX(100%);
  }
  input:checked ~ .toggle-path {
    @apply bg-magenta-80;
  }
</style>

<div class="flex flex-row">
  <div>Non</div>
  <div class="relative">
    <input type="checkbox" bind:checked class="hidden" />
    <!-- path -->
    <div class="h-5 bg-gray-200 rounded-full shadow-inner toggle-path w-9" />
    <!-- circle -->
    <div
      class="absolute inset-y-0 left-0 w-4 h-4 bg-white rounded-full shadow toggle-circle" />
  </div>
  <div>Oui</div>
</div>
