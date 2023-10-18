<script lang="ts">
  import {
    currentFormData,
    currentSchema,
    isRequired,
  } from "$lib/validation/validation";
  import FieldWrapper from "../field-wrapper.svelte";
  import { addIcon } from "$lib/icons";
  import type { CustomChoice, CustomizableFK } from "$lib/types";
  import Button from "../../display/button.svelte";
  import Select from "../../inputs/select/select.svelte";

  export let id: string;
  export let values: CustomizableFK[];

  export let disabled = false;
  export let readonly = $currentSchema?.[id]?.readonly;
  export let placeholder = "";

  // Spécifiques
  export let addButtonLabel: string | undefined = undefined;
  export let choices: CustomChoice[];
  export let sort = false;
  export let onChange: ((newValues: string[]) => void) | undefined = undefined;
  export let placeholderMulti = "";
  export let canAdd = true;
  export let structureSlug: string | undefined = undefined;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;

  let textInputVisible = false;
  let newValue: string;

  const maxLength = 140;

  let filteredChoices = choices;
  $: filteredChoices = choices.filter(
    (choice) => choice.structure == null || choice.structure === structureSlug
  );

  function handleAddValue() {
    const value = newValue;
    if (value.length > maxLength) {
      return;
    }
    choices = [...choices, { value, label: value }];
    values = [...values, value];
    newValue = "";
    textInputVisible = false;
  }
</script>

{#if $currentSchema && id in $currentSchema}
  <FieldWrapper
    {id}
    let:onBlur
    let:errorMessages
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    {readonly}
  >
    <Select
      {id}
      bind:value={values}
      on:blur={onBlur}
      choices={filteredChoices}
      {onChange}
      {sort}
      {placeholder}
      {placeholderMulti}
      {disabled}
      {readonly}
      {errorMessages}
      multiple
    />
    {#if canAdd}
      <div class="flex flex-col" class:mt-s12={canAdd}>
        <div class:hidden={textInputVisible}>
          <Button
            label={addButtonLabel || "Ajouter une autre option"}
            icon={addIcon}
            noBackground
            small
            on:click={() => (textInputVisible = true)}
          />
        </div>
        <div class="flex flex-row gap-s16" class:hidden={!textInputVisible}>
          <div class="flex-grow">
            <div class="flex flex-col">
              <input
                id={`${id}-text-input`}
                name={`${id}-text-input`}
                type="text"
                bind:value={newValue}
                maxlength={maxLength}
              />
              {#if newValue && maxLength != null}
                <div
                  class="mt-s4 self-end text-f12 text-gray-text"
                  class:text-error={newValue?.length > maxLength}
                >
                  {newValue.length}/{maxLength} caractères
                </div>
              {/if}
            </div>
          </div>
          <div class="self-center">
            <div class="flex flex-col gap-s8 md:flex-row">
              <Button
                label="Ajouter"
                small
                disabled={!newValue}
                on:click={handleAddValue}
              />
              <Button
                label="Annuler"
                secondary
                small
                on:click={() => (textInputVisible = false)}
              />
            </div>
          </div>
        </div>
      </div>
    {/if}
  </FieldWrapper>
  <div />
{/if}
