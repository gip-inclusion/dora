<script lang="ts">
  import type { Shape } from "$lib/validation/schemas/utils";
  import FieldWrapper from "./field-wrapper.svelte";

  export let id: string;
  export let schema: Shape<string | number>;
  export let type: "email" | "tel" | "text" | "url" | "date" | "number" =
    "text";
  export let value: any | undefined = undefined;
  export let autocomplete = undefined;
  export let disabled = false;
  export let readonly = schema?.readonly;
  export let placeholder: string | undefined = undefined;

  // Specifique
  export let maxLength: number | undefined = schema?.maxLength;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;

  export let vertical = false;

  $: props = {
    id,
    name: id,
    autocomplete,
    disabled,
    readonly,
    placeholder,
  };
</script>

{#if schema}
  <FieldWrapper
    {id}
    let:onBlur
    let:onChange
    label={schema.label}
    {description}
    {hidden}
    {hideLabel}
    required={schema.required}
    {vertical}
    {readonly}
    {disabled}
  >
    <slot slot="description" name="description" />

    <div class="flex flex-col">
      {#if type === "text"}
        <input
          type="text"
          bind:value
          on:blur={onBlur}
          on:change={onChange}
          {...props}
        />
      {:else if type === "date"}
        <input
          type="text"
          bind:value
          on:blur={onBlur}
          on:change={onChange}
          {...props}
        />
      {:else if type === "number"}
        <input
          type="number"
          bind:value
          on:blur={onBlur}
          on:change={onChange}
          {...props}
        />
      {:else if type === "email"}
        <input
          type="email"
          bind:value
          on:blur={onBlur}
          on:change={onChange}
          {...props}
        />
      {:else if type === "tel"}
        <input
          type="tel"
          bind:value
          on:blur={onBlur}
          on:change={onChange}
          {...props}
        />
      {:else if type === "url"}
        <input
          type="url"
          bind:value
          on:blur={onBlur}
          on:change={onChange}
          {...props}
        />
      {:else if type === "date"}
        <input
          type="date"
          bind:value
          on:blur={onBlur}
          on:change={onChange}
          {...props}
        />
      {/if}
      {#if value && maxLength != null && !readonly && !disabled}
        <div
          class="mt-s4 self-end text-f12 text-gray-text-alt"
          class:text-error={value.length > maxLength}
        >
          {value?.length}/{maxLength} caractères
        </div>
      {/if}
    </div>
  </FieldWrapper>

  <style lang="postcss">
    input[type="text"],
    input[type="number"],
    input[type="url"],
    input[type="email"],
    input[type="tel"],
    input[type="date"] {
      @apply h-s48 rounded border border-gray-03 px-s12 py-s6 text-f14 placeholder-gray-text-alt outline-none focus:shadow-focus;
    }

    input {
      @apply grow read-only:text-gray-03 disabled:bg-gray-00;
    }
  </style>
{/if}
