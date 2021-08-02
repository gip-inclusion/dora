<script>
  import Field from "./field.svelte";

  export let value = undefined;
  export let selectedItems = undefined;

  export let type;
  export let field;

  export let placeholder = "";
  export let description = "";
  export let minValue = null;

  export let hideLabel = false;
</script>

<Field
  bind:value
  bind:selectedItems
  required={field.required}
  label={field.label}
  choices={field.child?.choices || field.choices}
  {type}
  {placeholder}
  {description}
  {hideLabel}
  {minValue} />
