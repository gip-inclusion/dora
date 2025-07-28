<script lang="ts">
  import type { Choice } from "$lib/types";
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import Select from "../../inputs/select/select.svelte";

  interface Props {
    id: string;
    value?: string[] | number[];
    disabled?: boolean;
    readonly?: any;
    placeholder?: string;
    initialValue?: any;
    // Spécifique du select
    choices: Choice[];
    sort?: boolean;
    onChange?: (newValues: string[]) => void;
    placeholderMulti?: string;
    fixedItemsValues?: string[];
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
    placeholder = "Choisir",
    initialValue = undefined,
    choices,
    sort = false,
    onChange,
    placeholderMulti = "Choisir",
    fixedItemsValues = [],
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
    {#snippet children({ onBlur, errorMessages })}
      <Select
        bind:value
        onblur={onBlur}
        {id}
        {choices}
        {fixedItemsValues}
        {onChange}
        {sort}
        {placeholder}
        {placeholderMulti}
        {disabled}
        {readonly}
        {initialValue}
        {errorMessages}
        multiple
      />
    {/snippet}
  </FieldWrapper>
{/if}
