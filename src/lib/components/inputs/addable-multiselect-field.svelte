<script lang="ts">
  import { addIcon } from "$lib/icons";
  import type { CustomChoice, CustomizableFK } from "$lib/types";
  import type { Shape } from "$lib/validation/schemas/utils";
  import Button from "../display/button.svelte";
  import BasicInputField from "./basic-input-field.svelte";
  import FieldWrapper from "./field-wrapper.svelte";
  import Select from "./select/select.svelte";

  export let id: string;
  export let schema: Shape<CustomizableFK[]>;
  export let disabled = false;
  export let readonly = schema?.readonly;
  export let placeholder = "";

  // Spécifiques
  export let addButtonLabel: string | undefined = undefined;
  export let choices: CustomChoice[];
  export let sort = false;
  export let onChange: ((newValues: string[]) => void) | undefined = undefined;
  export let placeholderMulti = "";
  export let canAdd = true;
  export let values: CustomizableFK[];
  export let structureSlug: string | undefined = undefined;

  let textInputVisible = false;
  let newValue: string;

  // Proxy vers le FieldWrapper
  export let description = "";
  export let hidden = false;
  export let hideLabel = false;
  export let vertical = false;

  const maxLength = 140;

  let filteredChoices = choices;
  $: filteredChoices = choices.filter(
    (c) => c.structure == null || c.structure === structureSlug
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

{#if schema}
  <FieldWrapper
    {id}
    let:onBlur
    label={schema.label}
    {description}
    {hidden}
    {hideLabel}
    required={schema.required}
    {vertical}
    {disabled}
    {readonly}
  >
    <Select
      {id}
      choices={filteredChoices}
      bind:value={values}
      on:blur={onBlur}
      {onChange}
      {sort}
      {placeholder}
      {placeholderMulti}
      {disabled}
      {readonly}
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
        <div class="flex flex-row gap-s16 " class:hidden={!textInputVisible}>
          <div class="flex-grow">
            <BasicInputField
              id={`${id}-text-input`}
              schema={{ label: "" }}
              type="text"
              bind:value={newValue}
              hideLabel
              vertical
              {maxLength}
            />
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
