<script lang="ts">
  import type { Choice } from "$lib/types";
  import type { Shape } from "$lib/validation/schemas/utils";
  import FieldWrapper from "./field-wrapper.svelte";
  import Select from "./select/select.svelte";

  export let id: string;
  export let schema: Shape<string | number>;

  export let value: string | number | undefined = undefined;
  export let disabled = false;
  export let readonly = schema?.readonly;
  export let placeholder = "";
  export let initialValue = undefined;

  // Spécifique du select
  export let choices: Choice[];
  export let sort = false;
  export let onChange = undefined;
  export let placeholderMulti = "";

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;
</script>

{#if schema}
  <FieldWrapper
    {id}
    let:onBlur
    label={schema.label}
    {description}
    {hidden}
    {hideLabel}
    required={schema.required}
    {vertical}
    {disabled}
    {readonly}
  >
    <Select
      {id}
      {choices}
      {sort}
      bind:value
      on:blur={onBlur}
      {onChange}
      {placeholder}
      {placeholderMulti}
      {disabled}
      {readonly}
      {initialValue}
    />
  </FieldWrapper>
{/if}
