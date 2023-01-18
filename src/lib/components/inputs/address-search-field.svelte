<script lang="ts">
  import StreetSearch from "./geo/street-search.svelte";
  import FieldWrapper from "./field-wrapper.svelte";
  import type { Shape } from "$lib/validation/schemas/utils";

  export let id: string;
  export let schema: Shape<string>;

  export let value: string | undefined = undefined;
  export let disabled = false;
  export let readonly = schema?.readonly;
  export let placeholder = "";
  export let initialValue = "";

  // Spécifiques:
  export let cityCode: string;
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
    <StreetSearch
      bind:value
      {onChange}
      {cityCode}
      {initialValue}
      {id}
      {disabled}
      {readonly}
      {placeholder}
    />
  </FieldWrapper>
{/if}
