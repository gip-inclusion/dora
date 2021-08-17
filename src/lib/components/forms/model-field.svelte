<script>
  import Field from "./field.svelte";

  export let value = undefined;
  export let selectedItem = undefined;
  export let label = undefined;
  export let type;
  export let field;
  export let vertical = false;
  export let errorMessage = undefined;

  export let disabled = undefined;
  export let visible = true;
  export let placeholder = "";
  export let description = "";
  export let minValue = null;

  export let hideLabel = false;
</script>

<Field
  bind:value
  bind:selectedItem
  on:input
  {errorMessage}
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
  {visible}
  {vertical}>
  <slot name="custom-input" slot="custom-input" />
  <slot name="helptext" slot="helptext" />
</Field>
