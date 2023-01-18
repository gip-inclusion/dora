<script lang="ts">
  import type { Shape } from "$lib/validation/schemas/utils";
  import FieldWrapper from "./field-wrapper.svelte";

  export let id: string;
  export let schema: Shape<string>;

  export let value;
  export let autocomplete = "";
  export let disabled = false;
  export let readonly = schema?.readonly;
  export let placeholder: string | undefined = undefined;
  export let rows = 4;

  // Specifique
  export let maxLength: number | undefined = schema?.maxLength;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;
</script>

{#if schema}
  <FieldWrapper
    let:onBlur
    {id}
    label={schema.label}
    {description}
    {hidden}
    {hideLabel}
    required={schema.required}
    {vertical}
    {readonly}
    {disabled}
    ><div class="flex flex-col">
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
      />
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
{/if}

<style lang="postcss">
  textarea {
    @apply min-h-[3rem] rounded border border-gray-03 px-s12 py-s6 text-f14 placeholder-gray-text-alt outline-none focus:shadow-focus;
    @apply grow read-only:text-gray-03 disabled:bg-gray-00;
  }
</style>
