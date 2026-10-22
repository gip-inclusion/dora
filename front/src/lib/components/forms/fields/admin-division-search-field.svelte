<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "#lib/validation/validation.js";
  import FieldWrapper from "../field-wrapper.svelte";
  import AdminDivisionSearch from "../../inputs/geo/admin-division-search.svelte";
  import type { GeoApiValue } from "#lib/types.js";

  interface Props {
    id: string;
    value?: string;
    disabled?: boolean;
    readonly?: boolean;
    placeholder?: string;
    initialValue?: string;
    // Spécifiques:
    searchType: string;
    onChange: (adminDetails: GeoApiValue) => void;
    choices: any;
    // Proxy vers le FieldWrapper
    description?: string;
    hidden?: boolean;
    hideLabel?: boolean;
    vertical?: boolean;
  }

  let {
    id,
    value = $bindable(),
    disabled = false,
    readonly,
    placeholder = "",
    initialValue = "",
    searchType,
    onChange,
    choices = $bindable(),
    description = "",
    hidden = false,
    hideLabel = false,
    vertical = false,
  }: Props = $props();
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    descriptionText={description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    readonly={readonly ?? $currentSchema?.[id]?.readonly}
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
