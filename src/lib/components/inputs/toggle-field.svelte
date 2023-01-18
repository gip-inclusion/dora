<script lang="ts">
  import type { Shape } from "$lib/validation/schemas/utils";
  import FieldWrapper from "./field-wrapper.svelte";
  import Toggle from "./others/toggle.svelte";

  export let id: string;
  export let schema: Shape<boolean>;

  export let value;
  export let disabled = false;
  export let readonly = schema?.readonly;

  // Spécifiques
  export let yesLabel: string | undefined = undefined;
  export let noLabel: string | undefined = undefined;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;

  if (!schema) {
    console.error("No schema for field", id);
  }
</script>

{#if schema}
  <FieldWrapper
    let:onBlur
    let:onChange
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
    <Toggle
      {id}
      bind:checked={value}
      on:change={onChange}
      {disabled}
      {readonly}
      {yesLabel}
      {noLabel}
    />
  </FieldWrapper>
{/if}
