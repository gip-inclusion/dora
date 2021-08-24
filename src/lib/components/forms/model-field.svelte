<script>
  import Field from "./field.svelte";

  export let value = undefined;
  export let name;
  export let label = undefined;
  export let type;
  export let field;
  export let choices = null;
  export let vertical = false;
  export let errorMessages = undefined;
  export let onSelectChange = undefined;

  export let disabled = undefined;
  export let readonly = false;
  export let visible = true;
  export let placeholder = "";
  export let description = "";
  export let minValue = null;

  export let hideLabel = false;
</script>

<Field
  bind:value
  {onSelectChange}
  {name}
  {errorMessages}
  required={field.required}
  maxLength={field.maxLength}
  label={label || field.label}
  choices={choices != null ? choices : field.child?.choices || field.choices}
  {type}
  {placeholder}
  {description}
  {hideLabel}
  {minValue}
  {disabled}
  {readonly}
  {visible}
  {vertical}>
  <slot name="custom-input" slot="custom-input" />
  <slot name="helptext" slot="helptext" />
</Field>
