<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import RichText from "$lib/components/inputs/rich-text/editor.svelte";

  export let id: string;
  export let value: string;

  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;
  export let placeholder = "";

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;

  let editor: RichText;

  export function updateValue(newValue: string) {
    editor.updateValue(newValue);
  }
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    let:onBlur
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    {readonly}
  >
    <RichText
      bind:this={editor}
      bind:htmlContent={value}
      initialContent={value}
      {id}
      name={id}
      {disabled}
      {readonly}
      {placeholder}
    />
  </FieldWrapper>
{/if}
