<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let id, group, choices, disabled, name, readonly;

  const dispatch = createEventDispatcher();

  let focusValue = undefined;

  // We want the change event to come from this component, not from
  // the individual checkboxes, in order to be able to validate properly
  function handleChange() {
    dispatch("change", name);
  }
</script>

<div {id} class="flex flex-col gap-s8">
  {#each choices as choice, i}
    <label
      class:outline={choice.value === focusValue}
      class="flex flex-row items-center"
    >
      <input
        id={`${id}-${i}`}
        bind:group
        on:change={handleChange}
        on:focus={() => (focusValue = choice.value)}
        on:blur={() => (focusValue = undefined)}
        value={choice.value}
        type="checkbox"
        class="sr-only"
        {disabled}
        {readonly}
      />
      <div
        class="flex h-s24 w-s24 shrink-0 justify-center rounded border border-gray-03"
      >
        <div class="hidden h-s12 w-s12 self-center bg-magenta-cta" />
      </div>
      <span class="ml-s16 inline-block text-f14 text-gray-text"
        >{choice.label}</span
      >
    </label>
  {/each}
</div>

<style lang="postcss">
  input[type="checkbox"]:checked + div div {
    @apply block;
  }
  label {
    @apply rounded p-s2;
  }
  .outline {
    outline: solid 2px #0a76f6;
  }
</style>
