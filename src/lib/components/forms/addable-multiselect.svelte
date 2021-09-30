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

  $: filteredChoices = choices.filter(
    (c) => c.structure == null || c.structure === structure
  );

  function handleAddValue() {
    const value = newValue;
    choices = [
      ...choices,
      {
        value,
        label: value,
      },
    ];
    values = [...values, value];

    textInputVisible = false;
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
    {sortSelect}>
    <slot name="helptext" slot="helptext" />
  </ModelField>
  <Field type="custom">
    <div slot="custom-input" class="mt-2 flex flex-col">
      <div class:hidden={textInputVisible}>
        <Button
          label="Ajouter une autre option"
          secondary
          nogrow
          small
          on:click={() => (textInputVisible = true)} />
      </div>
      <div class="flex flex-row gap-2 " class:hidden={!textInputVisible}>
        <Field type="text" bind:value={newValue} vertical />
        <div class="self-center">
          <div class="flex flex-col gap-1">
            <Button
              label="Ajouter"
              nogrow
              small
              disabled={!newValue}
              on:click={handleAddValue} />

            <Button
              label="Annuler"
              secondary
              nogrow
              small
              on:click={() => (textInputVisible = false)} />
          </div>
        </div>
      </div>
    </div>
  </Field>
</div>
