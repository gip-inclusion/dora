<script lang="ts">
  import type { Choice } from "$lib/types";
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import Select from "../../inputs/select/select.svelte";

  export let id: string;
  export let value: string | number | undefined = undefined;

  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;
  export let placeholder = "";
  export let initialValue = undefined;

  // Spécifique du select
  export let choices: Choice[];
  export let sort = false;
  export let onChange = undefined;
  export let placeholderMulti = "";

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
    let:errorMessages
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {readonly}
    {disabled}
  >
    <Select
      {id}
      {choices}
      {sort}
      bind:value
      on:blur={onBlur}
      {onChange}
      {placeholder}
      {placeholderMulti}
      {disabled}
      {readonly}
      {initialValue}
      {errorMessages}
    />
  </FieldWrapper>
{/if}
