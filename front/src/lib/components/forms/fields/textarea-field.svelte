<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    formatErrors,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";

  interface Props {
    id: string;
    value: string;
    autocomplete?: any;
    disabled?: boolean;
    readonly?: any;
    placeholder?: string | undefined;
    // Specifique
    maxLength?: number | undefined;
    rows?: number;
    // Proxy vers le FieldWrapper
    description?: string;
    hidden?: boolean;
    hideLabel?: boolean;
    label?: any;
    vertical?: boolean;
  }

  let {
    id,
    value = $bindable(),
    autocomplete = undefined,
    disabled = false,
    readonly = undefined,
    placeholder = undefined,
    maxLength = undefined,
    rows = 4,
    description = "",
    hidden = false,
    hideLabel = false,
    label = undefined,
    vertical = false,
  }: Props = $props();
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    label={label ?? $currentSchema?.[id]?.label}
    required={isRequired($currentSchema[id], $currentFormData)}
    descriptionText={description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    readonly={readonly ?? $currentSchema?.[id]?.readonly}
  >
    {#snippet children({ onBlur, errorMessages })}
      <div class="flex flex-col">
        <textarea
          bind:value
          onblur={onBlur}
          {id}
          name={id}
          {autocomplete}
          {disabled}
          {readonly}
          {placeholder}
          {rows}
          maxlength={maxLength ?? $currentSchema?.[id]?.maxLength}
          aria-describedby={formatErrors(id, errorMessages)}
          class="border-gray-03 px-s12 py-s6 text-f16 placeholder-gray-text-alt focus:shadow-focus read-only:text-gray-03 disabled:bg-gray-00 min-h-[3rem] grow rounded-sm border outline-hidden"
        ></textarea>
        {#if value && maxLength != null && !readonly && !disabled}
          <div
            class="mt-s4 text-f12 text-gray-text self-end"
            class:text-error={value.length > maxLength}
          >
            {value.length}/{maxLength} caractères
          </div>
        {/if}
      </div>
    {/snippet}
  </FieldWrapper>
{/if}
