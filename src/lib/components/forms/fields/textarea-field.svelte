<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    formatErrors,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";

  export let id: string;
  export let value: string;

  export let autocomplete = undefined;
  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;
  export let placeholder: string | undefined = undefined;

  // Specifique
  export let maxLength: number | undefined = $currentSchema?.[id]?.maxLength;
  export let rows = 4;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let label = $currentSchema?.[id]?.label;
  export let vertical = false;
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    let:onBlur
    let:errorMessages
    {label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    {readonly}
  >
    <div class="flex flex-col">
      <textarea
        bind:value
        on:blur={onBlur}
        {id}
        name={id}
        {autocomplete}
        {disabled}
        {readonly}
        {placeholder}
        {rows}
        maxlength={maxLength}
        aria-describedby={formatErrors(id, errorMessages)}
      />
      {#if value && maxLength != null && !readonly && !disabled}
        <div
          class="mt-s4 self-end text-f12 text-gray-text"
          class:text-error={value.length > maxLength}
        >
          {value.length}/{maxLength} caractères
        </div>
      {/if}
    </div>
  </FieldWrapper>
{/if}

<style lang="postcss">
  textarea {
    @apply min-h-[3rem] rounded border border-gray-03 px-s12 py-s6 text-f14 placeholder-gray-text-alt outline-none focus:shadow-focus;
    @apply grow read-only:text-gray-03 disabled:bg-gray-00;
  }
</style>
