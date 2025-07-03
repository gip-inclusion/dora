<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import CitySearch from "../../inputs/geo/city-search.svelte";
  import type { GeoApiValue } from "$lib/types";



  

  
  interface Props {
    id: string;
    disabled?: boolean;
    readonly?: any;
    initialValue?: string;
    // Spécifique
    onChange: (newValue: GeoApiValue) => void;
    // Proxy vers le FieldWrapper
    description?: string;
    hidden?: boolean;
    hideLabel?: boolean;
    vertical?: boolean;
  }

  let {
    id,
    disabled = false,
    readonly = $currentSchema?.[id]?.readonly,
    initialValue = "",
    onChange,
    description = "Commencez à saisir le nom et choisissez dans la liste.",
    hidden = false,
    hideLabel = false,
    vertical = false
  }: Props = $props();
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
    {#snippet children({ onBlur })}
        <CitySearch on:blur={onBlur} {id} {onChange} {initialValue} {disabled} />
          {/snippet}
    </FieldWrapper>
{/if}
