<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import StreetSearch from "../../inputs/geo/street-search.svelte";

  export let id: string;
  export let value: string | undefined = undefined;

  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;
  export let placeholder = "";
  export let initialValue = "";

  // Spécifiques:
  export let cityCode: string;
  export let onChange: (newValue: string) => void;

  // Proxy vers le FieldWrapper
  export let description =
    "Commencez à saisir le nom et choisissez dans la liste.";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    {readonly}
  >
    <StreetSearch
      {id}
      bind:value
      {onChange}
      {cityCode}
      {initialValue}
      {disabled}
      {readonly}
      {placeholder}
    />
  </FieldWrapper>
{/if}
