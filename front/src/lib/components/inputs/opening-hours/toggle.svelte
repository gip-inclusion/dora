<script lang="ts">
  import { createEventDispatcher } from "svelte";

  // https://tailwindcomponents.com/component/toggle-button-1
  export let id: string;
  export let checked: boolean | undefined = undefined;
  export let disabled = false;
  export let readonly = false;
  export let yesLabel = "Oui";
  export let noLabel = "Non";

  const dispatcher = createEventDispatcher();

  function handleKeyDown(event) {
    if (event.code === "Space" || event.code === "Enter") {
      checked = !checked;
      event.preventDefault();
    }
    if (event.code === "Escape") {
      event.target.blur();
    }
  }
</script>

<div
  class="mt-s8 relative flex flex-row items-center self-start"
  on:click={() => {
    checked = !checked;
    dispatcher("change");
  }}
  on:keydown={handleKeyDown}
  tabindex="0"
  role="radio"
  aria-checked={checked}
>
  <input
    {id}
    name={id}
    type="checkbox"
    bind:checked
    on:change
    class="hidden"
    {disabled}
    {readonly}
  />
  <!-- path -->
  <span
    class="toggle-path h-s24 w-s40 border-gray-03 inline-block shrink-0 rounded-full border bg-white"
  />
  <!-- circle -->
  <span
    class="toggle-circle inset-y-s0 left-s0 h-s16 w-s16 bg-gray-text-alt absolute inline-block shrink-0 rounded-full"
  />
  <span class="ml-s8 pb-s2 text-f14 text-gray-text">
    {#if checked}
      <span class="text-magenta-cta">{yesLabel}</span>
    {:else}
      <span class="text-gray-text">{noLabel}</span>
    {/if}
  </span>
</div>

<style lang="postcss">
  @reference "../../../../app.css";

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
