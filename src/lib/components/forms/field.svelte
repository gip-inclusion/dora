<script lang="ts">
  import {
    contextValidationKey,
    type ValidationContext,
  } from "$lib/validation";
  import { getContext } from "svelte";
  import Alert from "./alert.svelte";
  import Input from "./input.svelte";

  export let value = undefined;
  export let name = "";
  export let type;
  export let errorMessages = [];
  export let allowHTMLError = false;
  export let autocomplete = undefined;
  export let passwordrules = undefined;
  export let vertical = false;
  export let label = "";
  export let required = false;
  export let maxLength = undefined;
  export let rows = undefined;
  export let choices = [];
  export let sortSelect = undefined;

  export let disabled = undefined;
  export let readonly = false;
  export let placeholder = undefined;
  export let placeholderMulti = undefined;
  export let initialValue = undefined;
  export let description = "";
  export let minValue = undefined;

  export let hideLabel = false;

  export let onSelectChange = undefined;

  let field;

  export function updateValue(v) {
    field.updateValue(v);
  }

  const context = getContext<ValidationContext>(contextValidationKey);

  function handleBlur(evt) {
    if (context) context.onBlur(evt);
  }

  function handleChange(evt) {
    if (context) context.onChange(evt);
  }
</script>

<div
  {name}
  class="items-top flex flex-col gap-s8"
  class:lg:flex-row={!vertical}
  class:hidden={type === "hidden"}
  isDOMLabel={type !== "checkboxes" && type !== "radios"}
>
  <!-- #1# -->
  <div class="flex flex-col{vertical ? '' : ' lg:w-1/4'}">
    <label for={name} class="flex">
      <h4 class="my-s4 first-letter:capitalize" class:hidden={hideLabel}>
        {label}
      </h4>
      {#if required} <span class="ml-s6 text-error"> *</span>{/if}</label
    >
    {#if description}
      <small>{description}</small>
    {/if}
  </div>
  <div class="flex flex-col{vertical ? '' : ' lg:w-3/4'}">
    {#if type !== "custom"}
      <Input
        bind:this={field}
        bind:value
        on:blur={handleBlur}
        on:change={handleChange}
        on:change
        on:input
        {onSelectChange}
        {type}
        {name}
        {choices}
        {sortSelect}
        {maxLength}
        {rows}
        {placeholder}
        {placeholderMulti}
        {initialValue}
        {minValue}
        {disabled}
        {readonly}
        {autocomplete}
        {passwordrules}
      />
      <slot name="custom-input" />
    {:else}
      <slot name="custom-input" />
    {/if}
    {#each errorMessages || [] as msg}
      <Alert label={msg} isHTML={allowHTMLError} />
    {/each}
  </div>
</div>
