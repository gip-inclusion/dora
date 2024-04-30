<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { formatErrors } from "$lib/validation/validation";

  import CheckboxMark from "../display/checkbox-mark.svelte";

  export let id,
    group,
    choices,
    disabled,
    name,
    readonly,
    horizontalCheckboxes = false,
    errorMessages: string[] = [];

  const dispatch = createEventDispatcher();

  let focusValue = undefined;

  // We want the change event to come from this component, not from
  // the individual checkboxes, in order to be able to validate properly
  function handleChange() {
    dispatch("change", name);
  }
</script>

<div {id} class="flex gap-s8" class:flex-col={!horizontalCheckboxes}>
  {#each choices as choice, i}
    <label
      class:outline={choice.value === focusValue}
      class="flex flex-row items-center"
      class:mr-s24={horizontalCheckboxes}
    >
      <input
        id={`${id}-${i}`}
        name={id}
        bind:group
        on:change={handleChange}
        on:focus={() => (focusValue = choice.value)}
        on:blur={() => (focusValue = undefined)}
        value={choice.value}
        type="checkbox"
        class="sr-only"
        {disabled}
        {readonly}
        aria-describedby={formatErrors(id, errorMessages)}
      />
      <CheckboxMark />
      <span class="ml-s16 inline-block text-f16 text-gray-text"
        >{choice.label}</span
      >
    </label>
  {/each}
</div>

<style lang="postcss">
  label {
    @apply rounded p-s2;
  }
  .outline {
    outline: solid 2px #0a76f6;
  }
</style>
