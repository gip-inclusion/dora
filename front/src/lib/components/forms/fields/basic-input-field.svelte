<!-- @migration-task Error while migrating Svelte code: This migration would change the name of a slot (description to description_1) making the component unusable -->
<script lang="ts">
  import type { Snippet } from "svelte";

  import { formatPhoneNumber } from "$lib/utils/misc";
  import {
    currentFormData,
    currentSchema,
    formatErrors,
    isRequired,
  } from "$lib/validation/validation";

  import FieldWrapper from "../field-wrapper.svelte";

  interface Props {
    id: string;
    value?: string;
    type?: "email" | "tel" | "text" | "url" | "date" | "number";
    autocomplete?: string;
    disabled?: boolean;
    readonly?: boolean;
    placeholder?: string;
    maxLength?: number;
    descriptionText?: string;
    hidden?: boolean;
    hideLabel?: boolean;
    vertical?: boolean;
    description?: Snippet;
  }

  let {
    id,
    value = $bindable(),
    type = "text",
    autocomplete = undefined,
    disabled = false,
    readonly = undefined,
    placeholder = undefined,
    maxLength = undefined,
    descriptionText = "",
    hidden = false,
    hideLabel = false,
    vertical = false,
    description,
  }: Props = $props();

  // Get readonly and maxLength from schema if not provided
  readonly = readonly ?? $currentSchema?.[id]?.readonly;
  maxLength = maxLength ?? $currentSchema?.[id]?.maxLength;

  let phoneValue = $state(value);

  function handlePhoneChange() {
    if (phoneValue) {
      phoneValue = phoneValue.toString().replace(/[^0-9]/g, "");
    }
    value = phoneValue;
  }

  function handlePhoneBlur() {
    if (phoneValue) {
      phoneValue = formatPhoneNumber(phoneValue.toString());
    }
  }

  function handlePhoneFocus() {
    if (phoneValue) {
      phoneValue = phoneValue.toString().replace(/[^0-9]/g, "");
    }
  }

  const commonProps = $derived({
    id,
    name: id,
    autocomplete,
    disabled,
    readonly,
    placeholder,
    maxLength,
  });

  const inputClasses =
    "h-s48 border-gray-03 px-s12 py-s6 text-f16 placeholder-gray-text-alt focus:shadow-focus rounded-sm border outline-hidden read-only:text-gray-03 disabled:bg-gray-00 grow";
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {descriptionText}
    {hidden}
    {hideLabel}
    {vertical}
    {readonly}
    {disabled}
    {description}
  >
    {#snippet children({ onBlur, onChange, errorMessages })}
      {@const props = {
        ...commonProps,
        "aria-describedby": formatErrors(id, errorMessages),
      }}

      <div class="flex flex-col">
        {#if type === "text"}
          <input
            type="text"
            class={inputClasses}
            bind:value
            on:blur={onBlur}
            on:change={onChange}
            {...props}
          />
        {:else if type === "date"}
          <input
            type="date"
            class={inputClasses}
            bind:value
            on:blur={onBlur}
            on:change={onChange}
            {...props}
          />
        {:else if type === "number"}
          <input
            type="text"
            class={inputClasses}
            bind:value
            on:blur={onBlur}
            on:change={onChange}
            inputmode="numeric"
            {...props}
          />
        {:else if type === "email"}
          <input
            type="email"
            class={inputClasses}
            bind:value
            on:blur={onBlur}
            on:change={onChange}
            {...props}
          />
        {:else if type === "tel"}
          <input
            type="tel"
            class={inputClasses}
            bind:value={phoneValue}
            on:blur={(evt) => {
              handlePhoneBlur();
              onBlur(evt);
            }}
            on:focus={handlePhoneFocus}
            on:input={handlePhoneChange}
            {...props}
            maxlength={null}
          />
        {:else if type === "url"}
          <input
            type="url"
            class={inputClasses}
            bind:value
            on:blur={onBlur}
            on:change={onChange}
            {...props}
          />
        {/if}
        {#if value && maxLength != null && !readonly && !disabled}
          <div
            class="mt-s4 text-f12 text-gray-text-alt self-end"
            class:text-error={value.toString().length > maxLength}
          >
            {value.toString().length}/{maxLength} caractères
          </div>
        {/if}
      </div>
    {/snippet}
  </FieldWrapper>
{/if}
