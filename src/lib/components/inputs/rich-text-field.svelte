<script lang="ts">
  import RichText from "$lib/components/inputs/rich-text/editor.svelte";
  import type { Shape } from "$lib/validation/schemas/utils";
  import FieldWrapper from "./field-wrapper.svelte";

  export let id: string;
  export let schema: Shape<string>;

  export let value;
  export let disabled = false;
  export let readonly = schema?.readonly;
  export let placeholder = "";

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;
  let editor;

  export function updateValue(newValue: string) {
    editor.updateValue(newValue);
  }
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
