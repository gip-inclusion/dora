<script lang="ts">
  import AutoComplete from "./simple-autocomplete.svelte";

  export let id: string;
  export let choices: { value: string | number; label: string }[] | undefined =
    undefined;
  export let fixedItemsValues: string[] = [];
  export let sort = false;
  export let value: string | number | string[] | number[] | undefined =
    undefined;
  export let searchText: string | undefined;
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
  export let onChange:
    | ((newValue: string) => void)
    | ((newValues: string[]) => void)
    | undefined = undefined;
  export let initialValue = undefined;
  export let showClear = true;
  export let errorMessages: string[] = [];
  export let extraClass = "";

  // https://github.com/sveltejs/svelte/issues/5604
  const hasPrependSlot = $$slots.prepend;
  const hasAppendSlot = $$slots.append;
  const hasCustomContentSlot = $$slots.itemContent;

  $: {
    if (sort) {
      choices = choices.sort((a, b) =>
        a.label.localeCompare(b.label, "fr", { numeric: true })
      );
    }
  }
</script>

<AutoComplete
  name={id}
  inputId={id}
  bind:value
  bind:text={searchText}
  on:blur
  {localFiltering}
  {minCharactersToSearch}
  {onChange}
  bind:items={choices}
  {fixedItemsValues}
  {initialValue}
  {disabled}
  {readonly}
  {placeholder}
  {placeholderMulti}
  {multiple}
  {searchFunction}
  {delay}
  className="rounded focus-within:shadow-focus {extraClass}"
  inputClassName="focus:outline-none border rounded border-gray-03"
  dropdownClassName="!top-[48px] rounded shadow-md"
  showLoadingIndicator
  {hideArrow}
  {showClear}
  {hasPrependSlot}
  {hasAppendSlot}
  {hasCustomContentSlot}
  {errorMessages}
>
  <slot name="prepend" slot="prepend" />

  <svelte:fragment slot="itemContent" let:item>
    <slot name="itemContent" {item} />
  </svelte:fragment>

  <slot name="append" slot="append" />
</AutoComplete>
