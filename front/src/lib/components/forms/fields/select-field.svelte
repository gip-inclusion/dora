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
    value?: string | number | undefined;
    disabled?: boolean;
    readonly?: any;
    placeholder?: string;
    initialValue?: string | undefined;
    // Spécifique du select
    choices: Choice[];
    searchFunction?: ((searchText: string) => Promise<Choice[]>) | undefined;
    sort?: boolean;
    onChange?: any;
    placeholderMulti?: string;
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
    placeholder = "Choisir",
    initialValue = undefined,
    choices,
    searchFunction = undefined,
    sort = false,
    onChange = undefined,
    placeholderMulti = "Choisir",
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
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {readonly}
    {disabled}
  >
    {#snippet children({ onBlur, errorMessages })}
      <Select
        {id}
        {choices}
        {sort}
        {searchFunction}
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
    {/snippet}
  </FieldWrapper>
{/if}
