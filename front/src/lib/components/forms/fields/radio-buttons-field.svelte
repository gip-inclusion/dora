<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import RadioButtons from "../../inputs/radio-buttons.svelte";



  

  
  interface Props {
    id: string;
    value: any;
    disabled?: boolean;
    readonly?: any;
    // Spécifiques
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
    readonly = $currentSchema?.[id]?.readonly,
    choices,
    description = "",
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
    {#snippet children({ onChange, errorMessages })}
        <RadioButtons
        bind:group={value}
        on:change={onChange}
        {id}
        name={id}
        {choices}
        {disabled}
        {readonly}
        {errorMessages}
      />
          {/snippet}
    </FieldWrapper>
{/if}
