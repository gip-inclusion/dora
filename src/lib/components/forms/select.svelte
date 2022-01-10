<script>
  import AutoComplete from "./simple-autocomplete.svelte";

  export let name = "";
  export let choices = undefined;
  export let sort = undefined;
  export let value = undefined;
  export let disabled = false;
  export let readonly = false;
  export let placeholder = "";
  export let placeholderMulti = "";
  export let multiple = false;
  export let hideArrow = false;
  export let searchFunction = undefined;
  export let delay = undefined;
  export let localFiltering = undefined;
  export let minCharactersToSearch = undefined;
  export let onChange = undefined;
  export let initialValue = undefined;
  export let postfixValueFunction = undefined;
  export let showClear = true;

  function getSortedChoices(items) {
    return items.sort((a, b) =>
      a.label.localeCompare(b.label, "fr", { numeric: true })
    );
  }
</script>

<AutoComplete
  {name}
  inputId={name}
  bind:value
  on:blur
  {localFiltering}
  {minCharactersToSearch}
  {onChange}
  items={sort ? getSortedChoices(choices) : choices}
  {initialValue}
  {disabled}
  {readonly}
  {placeholder}
  {placeholderMulti}
  {multiple}
  {searchFunction}
  {postfixValueFunction}
  {delay}
  className="rounded focus-within:shadow-focus"
  inputClassName="outline-none border rounded border-gray-03"
  dropdownClassName="mt-s16 rounded shadow-md"
  html5autocomplete={false}
  showLoadingIndicator
  {hideArrow}
  {showClear}
/>
