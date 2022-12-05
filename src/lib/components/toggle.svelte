<script lang="ts">
  // https://tailwindcomponents.com/component/toggle-button-1

  export let checked = undefined;
  export let disabled = false;
  export let readonly;
  export let name;
</script>

<!--
  That's a *second* label on the same input (the other one being the "real"
  label from field.svelte)
  This one is here only so that a click anywhere on the component will actually
  toggle the hidden checkbox.
  TODO: check accessibility, and maybe use
  https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Techniques/Using_the_aria-describedby_attribute
  Or just find a cleaner way to do it!
-->
<label class="relative flex flex-row self-start">
  <input
    id={name}
    {name}
    type="checkbox"
    bind:checked
    on:change
    class="hidden"
    {disabled}
    {readonly}
  />
  <!-- path -->
  <div
    class="toggle-path h-s24 w-s40 shrink-0 rounded-full border border-gray-03 bg-white"
  />
  <!-- circle -->
  <div
    class="toggle-circle absolute inset-y-s0 left-s0 h-s16 w-s16 shrink-0 rounded-full bg-gray-text-alt"
  />
  <div class="ml-s8 text-f14 text-gray-text">
    {checked ? "Oui" : "Non"}
  </div>
</label>

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

    @apply bg-magenta-cta;
  }

  input:checked ~ .toggle-path {
    @apply border-magenta-hover bg-magenta-20;
  }
</style>
