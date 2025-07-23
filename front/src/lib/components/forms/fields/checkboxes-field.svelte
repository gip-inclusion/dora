<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import Checkboxes from "../../inputs/checkboxes.svelte";

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
    horizontalCheckboxes?: boolean;
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
    vertical = false,
    horizontalCheckboxes = false,
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
    {#snippet children({ onChange, errorMessages })}
      <Checkboxes
        bind:group={value}
        onchange={(event) => onChange(event)}
        name={id}
        {choices}
        {disabled}
        {readonly}
        {horizontalCheckboxes}
        {errorMessages}
      />
    {/snippet}
  </FieldWrapper>
{/if}
