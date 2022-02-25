<script>
  import Field from "./field.svelte";

  export let value = undefined;
  export let name;
  export let label = undefined;
  export let type;
  export let schema;
  export let choices = [];
  export let sortSelect = undefined;
  export let vertical = false;
  export let errorMessages = undefined;
  export let onSelectChange = undefined;

  export let disabled = undefined;
  export let readonly = false;
  export let visible = true;
  export let placeholder = "";
  export let placeholderMulti = "";
  export let initialValue = undefined;
  export let description = "";
  export let minValue = null;

  export let hideLabel = false;
  export let toggleYesText = undefined;
  export let toggleNoText = undefined;
  export let autocomplete = undefined;
  export let passwordrules = undefined;
</script>

<Field
  bind:value
  on:change
  {onSelectChange}
  {name}
  {errorMessages}
  required={schema?.required}
  maxLength={schema?.maxLength}
  {label}
  {choices}
  {sortSelect}
  {type}
  {placeholder}
  {placeholderMulti}
  {initialValue}
  {description}
  {hideLabel}
  {minValue}
  {disabled}
  {readonly}
  {visible}
  {vertical}
  {toggleYesText}
  {toggleNoText}
  {autocomplete}
>
  <slot name="custom-input" slot="custom-input" />
  <slot name="helptext" slot="helptext" />
</Field>
