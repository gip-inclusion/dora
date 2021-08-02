<script>
  import AutoComplete from "simple-svelte-autocomplete";

  export let choices;
  export let value;
  export let selectedItems;
  export let disabled = false;
  export let placeholder = "";
  export let multiple = false;
</script>

<AutoComplete
  items={choices}
  bind:value
  bind:selectedItem={selectedItems}
  labelFieldName="displayName"
  valueFieldName="value"
  {disabled}
  {placeholder}
  {multiple}
  className="rounded focus-within:shadow-focus"
  inputClassName="outline-none "
  dropdownClassName="rounded"
  html5autocomplete={false}
  showLoadingIndicator />
