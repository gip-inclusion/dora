<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { formatErrors } from "$lib/validation/validation";

  import Checkbox from "./checkbox.svelte";

  export let name: string;
  export let group: string[];
  export let choices: { label: string; value: string }[];
  export let disabled = false;
  export let readonly = false;
  export let horizontalCheckboxes = false;
  export let errorMessages: string[] = [];

  const dispatch = createEventDispatcher();

  let focusValue: string | undefined = undefined;

  // We want the change event to come from this component, not from
  // the individual checkboxes, in order to be able to validate properly
  function handleChange() {
    dispatch("change", name);
  }
</script>

<div class="flex gap-s8" class:flex-col={!horizontalCheckboxes}>
  {#each choices as choice}
    <Checkbox
      {name}
      bind:group
      label={choice.label}
      value={choice.value}
      {disabled}
      {readonly}
      horizontal={horizontalCheckboxes}
      errorMessage={formatErrors(name, errorMessages)}
      focused={focusValue === choice.value}
      on:change={handleChange}
      on:focus={() => (focusValue = choice.value)}
      on:blur={() => (focusValue = undefined)}
    />
  {/each}
</div>
