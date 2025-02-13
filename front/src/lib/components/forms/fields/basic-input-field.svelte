<script lang="ts">
  import { formatPhoneNumber } from "$lib/utils/misc";
  import {
    currentFormData,
    currentSchema,
    formatErrors,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";

  export let id: string;
  export let value: string | undefined = undefined;

  export let type: "email" | "tel" | "text" | "url" | "date" | "number" =
    "text";
  export let autocomplete: string | undefined = undefined;
  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;
  export let placeholder: string | undefined = undefined;

  // Specifique
  export let maxLength: number | undefined = $currentSchema?.[id]?.maxLength;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;

  let phoneValue = value;
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

  $: commonProps = {
    id,
    name: id,
    autocomplete,
    disabled,
    readonly,
    placeholder,
    maxLength,
  };

  const inputClasses =
    "h-s48 border-gray-03 px-s12 py-s6 text-f16 placeholder-gray-text-alt focus:shadow-focus rounded-sm border outline-hidden read-only:text-gray-03 disabled:bg-gray-00 grow";
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    let:onBlur
    let:onChange
    let:errorMessages
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {readonly}
    {disabled}
  >
    <slot slot="description" name="description" />

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
  </FieldWrapper>
{/if}
