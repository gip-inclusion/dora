<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import StreetSearch from "../../inputs/geo/street-search.svelte";

  interface Props {
    id: string;
    value?: string;
    disabled?: boolean;
    readonly?: boolean;
    placeholder?: string;
    initialValue?: string;
    // Spécifiques:
    cityCode: string;
    onChange: (newValue: string) => void;
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
    cityCode,
    onChange,
    description = "Commencez à saisir le nom et choisissez dans la liste.",
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
