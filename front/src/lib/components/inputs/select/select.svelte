<script lang="ts">
  import type { Snippet } from "svelte";

  import AutoComplete from "./simple-autocomplete.svelte";

  type Choice = { value: string | number; label: string };

  interface Props {
    id: string;
    choices?: Choice[];
    fixedItemsValues?: string[];
    sort?: boolean;
    value?: string | number | string[] | number[];
    searchText?: string;
    disabled?: boolean;
    readonly?: boolean;
    placeholder?: string;
    placeholderMulti?: string;
    multiple?: boolean;
    hideArrow?: boolean;
    searchFunction?: (searchTxt: string) => Promise<Choice[]>;
    delay?: any;
    localFiltering?: any;
    minCharactersToSearch?: any;
    onblur?: (evt: FocusEvent) => void;
    onChange?: ((newValue: string) => void) | ((newValues: string[]) => void);
    initialValue?: string | number | string[] | number[];
    showClear?: boolean;
    errorMessages?: string[];
    extraClass?: string;
    prepend?: Snippet;
    append?: Snippet;
    itemContent?: Snippet<[any]>;
  }

  let {
    id,
    choices = $bindable([]),
    fixedItemsValues = [],
    sort = false,
    value = $bindable(undefined),
    searchText = $bindable(""),
    disabled = false,
    readonly = false,
    placeholder = "",
    placeholderMulti = "",
    multiple = false,
    hideArrow = false,
    searchFunction = undefined,
    delay = undefined,
    localFiltering = undefined,
    minCharactersToSearch = undefined,
    onblur = undefined,
    onChange = undefined,
    initialValue = undefined,
    showClear = true,
    errorMessages = [],
    extraClass = "",
    prepend,
    append,
    itemContent,
  }: Props = $props();

  $effect(() => {
    if (sort) {
      choices = choices.sort((a, b) =>
        a.label.localeCompare(b.label, "fr", { numeric: true })
      );
    }
  });
</script>

<AutoComplete
  name={id}
  inputId={id}
  bind:value
  bind:text={searchText}
  {onblur}
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
  className="rounded-sm focus-within:shadow-focus {extraClass}"
  inputClassName="focus:outline-hidden border rounded-sm border-gray-03"
  dropdownClassName="top-[48px]! rounded-sm shadow-md"
  showLoadingIndicator
  {hideArrow}
  {showClear}
  {errorMessages}
  {prepend}
  {itemContent}
  {append}
/>
