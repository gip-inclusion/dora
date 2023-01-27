<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import RadioButtons from "../../inputs/radio-buttons.svelte";

  export let id: string;
  export let value: boolean;

  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;

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

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    let:onBlur
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
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
      {disabled}
      {readonly}
    />
  </FieldWrapper>
{/if}
