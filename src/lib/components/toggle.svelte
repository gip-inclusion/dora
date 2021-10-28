<script>
  // https://tailwindcomponents.com/component/toggle-button-1

  export let checked = undefined;
  export let toggleYesText = "Oui";
  export let toggleNoText = "Non";
  export let disabled = false;
  export let readonly;
  export let name;
</script>

<style lang="postcss">
  .toggle-path {
    transition: all 0.15s ease-in-out;
  }

  .toggle-circle {
    top: 0.25rem;
    left: 0.25rem;
    transition: all 0.15s ease-in-out;
  }

  input:checked ~ .toggle-circle {
    transform: translateX(100%);

    @apply bg-dora-magenta-cta;
  }

  input:checked ~ .toggle-path {
    @apply border-dora-magenta-hover bg-magenta-20;
  }
</style>

<!--
  That's a *second* label on the same input (the other one being the "real"
  label from field.svelte)
  This one is here only so that a click anywhere on the component will actually
  toggle the hidden checkbox.
  TODO: check accessibility, and maybe use
  https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Techniques/Using_the_aria-describedby_attribute
  Or just find a cleaner way to do it!
-->
<label class="relative flex flex-row">
  <input
    id={name}
    {name}
    type="checkbox"
    bind:checked
    class="hidden"
    {disabled}
    {readonly}
  />
  <!-- path -->
  <div
    class="flex-shrink-0 w-5 h-3 bg-white border rounded-full toggle-path border-gray-03"
  />
  <!-- circle -->
  <div
    class="absolute inset-y-0 left-0 flex-shrink-0 w-2 h-2 rounded-full bg-gray-text-alt toggle-circle"
  />
  <div class="ml-1 text-sm text-gray-text">
    {@html checked ? toggleYesText : toggleNoText}
  </div>
</label>
