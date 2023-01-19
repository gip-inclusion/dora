<script lang="ts">
  import type { Shape } from "$lib/validation/schemas/utils";
  import FieldWrapper from "./field-wrapper.svelte";
  import RadioButtons from "./others/radio-buttons.svelte";

  export let id: string;
  export let schema: Shape<string[]>;

  export let value;
  export let disabled = false;
  export let readonly = schema?.readonly;

  // Spécifiques
  export let yesLabel = "Oui";
  export let noLabel = "Non";

  const choices = [
    { value: true, label: yesLabel },
    { value: false, label: noLabel },
  ];

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;
</script>

{#if schema}
  <FieldWrapper
    let:onBlur
    {id}
    label={schema.label}
    {description}
    {hidden}
    {hideLabel}
    required={schema.required}
    {vertical}
    {disabled}
    {readonly}
  >
    <RadioButtons
      {id}
      name={id}
      bind:group={value}
      on:change
      {choices}
      {yesLabel}
      {noLabel}
      {disabled}
      {readonly}
    />
  </FieldWrapper>
{/if}
