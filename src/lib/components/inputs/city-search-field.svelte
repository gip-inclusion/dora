<script lang="ts">
  import type { Shape } from "$lib/validation/schemas/utils";
  import FieldWrapper from "./field-wrapper.svelte";
  import CitySearch from "./geo/city-search.svelte";

  export let id: string;
  export let schema: Shape<string>;

  export let disabled = false;
  export let readonly = schema?.readonly;
  export let placeholder = "";
  export let initialValue = "";

  // Spécifique
  export let onChange: (newValue: string) => void;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;
</script>

{#if schema}
  <FieldWrapper
    let:onBlur
    {id}
    label={schema.label}
    {description}
    {hidden}
    {hideLabel}
    required={schema.required}
    {vertical}
    {disabled}
    {readonly}
  >
    <CitySearch
      on:blur={onBlur}
      {onChange}
      {initialValue}
      {id}
      {disabled}
      {placeholder}
    />
  </FieldWrapper>
{/if}
