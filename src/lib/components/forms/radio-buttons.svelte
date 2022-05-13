<script>
  import { createEventDispatcher } from "svelte";

  export let group, choices, disabled, name, readonly, inline;
  const dispatch = createEventDispatcher();

  // We want the change event to come from this component, not from
  // the individual checkboxes, in order to be able to validate properly
  function handleChange() {
    dispatch("change", name);
  }
</script>

<div
  class="flex"
  class:flex-col={!inline}
  class:gap-s8={!inline}
  class:gap-s24={inline}
>
  {#each choices as choice}
    <label class="flex flex-row items-center focus-within:shadow-focus">
      <input
        bind:group
        on:change={handleChange}
        type="radio"
        value={choice.value}
        class="hidden"
        {disabled}
        {readonly}
      />
      <div
        class="toggle-path flex h-s24 w-s24 justify-center rounded-full border border-gray-03 bg-white "
      >
        <div
          class="toggle-circle hidden h-s12 w-s12 self-center rounded-full bg-magenta-cta"
        />
      </div>
      <span class="ml-s16 inline-block text-f14 text-gray-text"
        >{choice.label}</span
      >
    </label>
  {/each}
</div>

<style lang="postcss">
  input[type="radio"]:checked + div div {
    @apply block;
  }
</style>
