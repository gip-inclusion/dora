<script lang="ts">
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
    onchange?: (event: Event) => void;
  }

  let {
    name,
    group = $bindable(),
    choices,
    disabled = false,
    readonly = false,
    horizontalCheckboxes = false,
    errorMessages = [],
    onchange,
  }: Props = $props();

  let focusValue: string | undefined = $state(undefined);
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
      {onchange}
      onfocus={() => (focusValue = choice.value)}
      onblur={() => (focusValue = undefined)}
    />
  {/each}
</div>
