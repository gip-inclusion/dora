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

  let textInputVisible = false;
  let newValue;

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
    {choices}
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
          <div class="flex flex-col">
            <Button
              label="Ajouter"
              secondary
              nogrow
              small
              on:click={handleAddValue} />

            <Button
              label="Annuler"
              tertiary
              nogrow
              small
              on:click={() => (textInputVisible = false)} />
          </div>
        </div>
      </div>
    </div>
  </Field>
</div>
