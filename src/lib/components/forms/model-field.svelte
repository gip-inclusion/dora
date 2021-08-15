<script>
  import Field from "./field.svelte";

  export let value = undefined;
  export let selectedItem = undefined;
  export let label;
  export let type;
  export let field;
  export let vertical = false;
  export let errors;
  export let errorMessages;

  export let disabled = undefined;
  export let placeholder = "";
  export let description = "";
  export let minValue = null;

  export let hideLabel = false;
</script>

<Field
  bind:value
  bind:selectedItem
  on:input
  {errors}
  {errorMessages}
  required={field.required}
  maxLength={field.maxLength}
  label={label || field.label}
  choices={field.child?.choices || field.choices}
  {type}
  {placeholder}
  {description}
  {hideLabel}
  {minValue}
  {disabled}
  {vertical}>
  <slot name="input" slot="name" />
  <slot name="helptext" slot="helptext" />
</Field>
