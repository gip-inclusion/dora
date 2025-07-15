<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import RichText from "$lib/components/inputs/rich-text/editor.svelte";

  interface Props {
    id: string;
    value: string;
    disabled?: boolean;
    readonly?: any;
    placeholder?: string;
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
    placeholder = "",
    description = "",
    hidden = false,
    hideLabel = false,
    vertical = false,
  }: Props = $props();

  let editor: RichText = $state();

  export function updateValue(newValue: string) {
    editor.updateValue(newValue);
  }
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
