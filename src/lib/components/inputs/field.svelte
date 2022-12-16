<script lang="ts">
  import type { InputType } from "$lib/types";
  import {
    contextValidationKey,
    type ValidationContext,
  } from "$lib/validation/validation";
  import { getContext } from "svelte";
  import Alert from "../display/alert.svelte";
  import Input from "./input.svelte";

  export let value = undefined;
  export let name = "";
  export let type: InputType | "custom";
  export let errorMessages = [];
  export let allowHTMLError = false;
  export let autocomplete = undefined;
  export let vertical = false;
  export let label = "";
  export let required = false;
  export let rows = undefined;
  export let choices = [];
  export let sortSelect = undefined;

  export let disabled = undefined;
  export let readonly = false;
  export let placeholder = undefined;
  export let placeholderMulti = undefined;
  export let initialValue = undefined;
  export let description = "";
  export let htmlDescription = false;
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
      <small
        >{#if htmlDescription}{@html description}{:else}{description}{/if}</small
      >
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
        {rows}
        {placeholder}
        {placeholderMulti}
        {initialValue}
        {minValue}
        {disabled}
        {readonly}
        {autocomplete}
      />
      <slot name="custom-input" />
    {:else}
      <slot name="custom-input" />
    {/if}
    {#each errorMessages || [] as msg}
      <Alert id="{name}-error" label={msg} isHTML={allowHTMLError} />
    {/each}
  </div>
</div>
