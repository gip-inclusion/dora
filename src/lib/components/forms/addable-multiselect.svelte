<script lang="ts">
  import Button from "../button.svelte";
  import Field from "./field.svelte";
  import SchemaField from "./schema-field.svelte";

  export let values;
  export let choices;
  export let errorMessages;
  export let sortSelect = false;
  export let name;
  export let label;
  export let placeholder;
  export let placeholderMulti;
  export let schema;
  export let structure = null;
  export let description = "";
  let canAdd = false;

  let textInputVisible = false;
  let newValue;
  let newValueErrors = [];

  // TODO: this should come from the schema
  const maxLength = 140;
  const errorMsg = `${maxLength} caractères maximum`;

  $: filteredChoices = choices.filter(
    (c) => c.structure == null || c.structure === structure
  );

  function handleAddValue() {
    const value = newValue;
    if (value.length > maxLength) {
      newValueErrors = [errorMsg];
      return;
    }

    choices = [...choices, { value, label: value }];
    values = [...values, value];
    newValue = "";
    textInputVisible = false;
  }

  function handleChangeValue(evt) {
    const length = evt.target.value.length;
    if (length > maxLength) {
      newValueErrors = [errorMsg];
    } else {
      newValueErrors = [];
    }
  }
</script>

<div>
  <SchemaField
    type="multiselect"
    {label}
    {placeholder}
    {placeholderMulti}
    {schema}
    {name}
    {errorMessages}
    bind:value={values}
    choices={filteredChoices}
    {sortSelect}
    {description}
  >
    <div slot="custom-input" class="flex flex-col" class:mt-s12={canAdd}>
      {#if canAdd}
        <div class:hidden={textInputVisible}>
          <Button
            label="Ajouter une autre option"
            secondary
            small
            on:click={() => (textInputVisible = true)}
          />
        </div>
        <div class="flex flex-row gap-s16 " class:hidden={!textInputVisible}>
          <Field
            {name}
            type="text"
            bind:value={newValue}
            on:input={handleChangeValue}
            errorMessages={newValueErrors}
            vertical
          />

          <div class="self-center">
            <div class="flex flex-col gap-s8">
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
      {/if}
    </div>
  </SchemaField>
</div>
