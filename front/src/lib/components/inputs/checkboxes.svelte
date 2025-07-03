<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { formatErrors } from "$lib/validation/validation";

  import Checkbox from "./checkbox.svelte";

  interface Props {
    name: string;
    group: string[];
    choices: { label: string; value: string }[];
    disabled?: boolean;
    readonly?: boolean;
    horizontalCheckboxes?: boolean;
    errorMessages?: string[];
  }

  let {
    name,
    group = $bindable(),
    choices,
    disabled = false,
    readonly = false,
    horizontalCheckboxes = false,
    errorMessages = []
  }: Props = $props();

  const dispatch = createEventDispatcher();

  let focusValue: string | undefined = $state(undefined);

  // We want the change event to come from this component, not from
  // the individual checkboxes, in order to be able to validate properly
  function handleChange() {
    dispatch("change", name);
  }
</script>

<div class="gap-s8 flex" class:flex-col={!horizontalCheckboxes}>
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
