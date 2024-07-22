<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import AdminDivisionSearch from "../../inputs/geo/admin-division-search.svelte";
  import type { GeoApiValue } from "$lib/types";

  export let id: string;
  export let value: string | undefined = undefined;

  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;
  export let placeholder = "";
  export let initialValue = "";

  // Spécifiques:
  export let searchType: string;
  export let onChange: (adminDetails: GeoApiValue) => void;
  export let choices;

  // Proxy vers le FieldWrapper
  export let description = "";
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
    <AdminDivisionSearch
      {id}
      {searchType}
      {onChange}
      {initialValue}
      bind:value
      bind:choices
      {placeholder}
      {disabled}
      {readonly}
    />
  </FieldWrapper>
{/if}
