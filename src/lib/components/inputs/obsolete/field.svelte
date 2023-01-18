<script lang="ts">
  import type { InputType } from "$lib/types";
  import {
    contextValidationKey,
    type ValidationContext,
  } from "$lib/validation/validation";
  import { getContext } from "svelte";
  import Alert from "../../display/alert.svelte";
  import Input from "./input.svelte";

  export let value: any | undefined = undefined;
  export let name = "";
  export let type: InputType | "custom";
  export let errorMessages = [];
  export let autocomplete = undefined;
  export let vertical = false;
  export let label = "";
  export let required = false;
  export let rows = undefined;
  export let choices: any[] | undefined = undefined;
  export let sortSelect: boolean | undefined = undefined;

  export let disabled = false;
  export let readonly = false;
  export let placeholder: string | undefined = undefined;
  export let placeholderMulti: string | undefined = undefined;
  export let initialValue = undefined;
  export let description = "";
  export let minValue = undefined;

  export let hideLabel = false;

  export let onChange = undefined;

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
      <small>{description}</small>
    {/if}
    <slot name="description" />
  </div>
  <div class="flex flex-col{vertical ? '' : ' lg:w-3/4'}">
    {#if type !== "custom"}
      <Input
        bind:value
        on:blur={handleBlur}
        on:change={handleChange}
        on:change
        on:input
        {onChange}
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
      <Alert id="{name}-error" label={msg} />
    {/each}
  </div>
</div>
