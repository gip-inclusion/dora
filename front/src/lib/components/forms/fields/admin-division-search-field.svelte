<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import AdminDivisionSearch from "../../inputs/geo/admin-division-search.svelte";
  import type { GeoApiValue } from "$lib/types";

  interface Props {
    id: string;
    value?: string | undefined;
    disabled?: boolean;
    readonly?: any;
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
    value = $bindable(undefined),
    disabled = false,
    readonly = $currentSchema?.[id]?.readonly,
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
