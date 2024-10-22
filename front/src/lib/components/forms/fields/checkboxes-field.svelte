<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import Checkboxes from "../../inputs/checkboxes.svelte";

  export let id: string;
  export let value;

  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;

  // Spécifiques
  export let choices;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;
  export let horizontalCheckboxes = false;
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    let:onChange
    let:errorMessages
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    {readonly}
  >
    <Checkboxes
      bind:group={value}
      on:change={onChange}
      name={id}
      {choices}
      {disabled}
      {readonly}
      {horizontalCheckboxes}
      {errorMessages}
    />
  </FieldWrapper>
{/if}
