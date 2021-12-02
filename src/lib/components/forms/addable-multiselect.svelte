<script>
  import Field from "./field.svelte";
  import ModelField from "./model-field.svelte";
  import Button from "../button.svelte";

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

    choices = [
      ...choices,
      {
        value,
        label: value,
      },
    ];
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
  <ModelField
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
  >
    <slot name="helptext" slot="helptext" />
  </ModelField>
  <Field type="custom">
    <div slot="custom-input" class="mt-s16 flex flex-col">
      <div class:hidden={textInputVisible}>
        <Button
          label="Ajouter une autre option"
          secondary
          nogrow
          small
          on:click={() => (textInputVisible = true)}
        />
      </div>
      <div class="flex flex-row gap-s16 " class:hidden={!textInputVisible}>
        <Field
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
              nogrow
              small
              disabled={!newValue}
              on:click={handleAddValue}
            />

            <Button
              label="Annuler"
              secondary
              nogrow
              small
              on:click={() => (textInputVisible = false)}
            />
          </div>
        </div>
      </div>
    </div>
  </Field>
</div>
