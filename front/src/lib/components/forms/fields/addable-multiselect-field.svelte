<script lang="ts">
  import { run } from "svelte/legacy";

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

  interface Props {
    id: string;
    values: CustomizableFK[];
    disabled?: boolean;
    readonly?: any;
    placeholder?: string;
    // Spécifiques
    addButtonLabel?: string | undefined;
    choices: CustomChoice[];
    sort?: boolean;
    onChange?: ((newValues: string[]) => void) | undefined;
    placeholderMulti?: string;
    canAdd?: boolean;
    structureSlug?: string | undefined;
    // Proxy vers le FieldWrapper
    description?: string;
    hidden?: boolean;
    hideLabel?: boolean;
    vertical?: boolean;
  }

  let {
    id,
    values = $bindable(),
    disabled = false,
    readonly = $currentSchema?.[id]?.readonly,
    placeholder = "Choisir",
    addButtonLabel = undefined,
    choices = $bindable(),
    sort = false,
    onChange = undefined,
    placeholderMulti = "Choisir",
    canAdd = true,
    structureSlug = undefined,
    description = "",
    hidden = false,
    hideLabel = false,
    vertical = false,
  }: Props = $props();

  let textInputVisible = $state(false);
  let newValue: string = $state();

  const maxLength = 140;

  let filteredChoices = $state(choices);
  run(() => {
    filteredChoices = choices.filter(
      (choice) => choice.structure == null || choice.structure === structureSlug
    );
  });

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
    label={$currentSchema[id].label}
    required={isRequired($currentSchema[id], $currentFormData)}
    {description}
    {hidden}
    {hideLabel}
    {vertical}
    {disabled}
    {readonly}
  >
    {#snippet children({ onBlur, errorMessages })}
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
          <div class="gap-s16 flex flex-row" class:hidden={!textInputVisible}>
            <div class="grow">
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
                    class="mt-s4 text-f12 text-gray-text self-end"
                    class:text-error={newValue?.length > maxLength}
                  >
                    {newValue.length}/{maxLength} caractères
                  </div>
                {/if}
              </div>
            </div>
            <div class="self-center">
              <div class="gap-s8 flex flex-col md:flex-row">
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
    {/snippet}
  </FieldWrapper>
  <div></div>
{/if}
