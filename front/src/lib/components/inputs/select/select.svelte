<script lang="ts">
  import { run } from 'svelte/legacy';

  import AutoComplete from "./simple-autocomplete.svelte";

  type Choice = { value: string | number; label: string };

  interface Props {
    id: string;
    choices?: Choice[] | undefined;
    fixedItemsValues?: string[];
    sort?: boolean;
    value?: string | number | string[] | number[] | undefined;
    searchText: string | undefined;
    disabled?: boolean;
    readonly?: boolean;
    placeholder?: string;
    placeholderMulti?: string;
    multiple?: boolean;
    hideArrow?: boolean;
    searchFunction?: 
    | ((searchTxt: string) => Promise<Choice[]>)
    | undefined;
    delay?: any;
    localFiltering?: any;
    minCharactersToSearch?: any;
    onChange?: 
    | ((newValue: string) => void)
    | ((newValues: string[]) => void)
    | undefined;
    initialValue?: any;
    showClear?: boolean;
    errorMessages?: string[];
    extraClass?: string;
    prepend?: import('svelte').Snippet;
    append?: import('svelte').Snippet;
    itemContent?: import('svelte').Snippet<[any]>;
  }

  let {
    id,
    choices = $bindable(undefined),
    fixedItemsValues = [],
    sort = false,
    value = $bindable(undefined),
    searchText = $bindable(),
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
    onChange = undefined,
    initialValue = undefined,
    showClear = true,
    errorMessages = [],
    extraClass = "",
    prepend,
    append,
    itemContent
  }: Props = $props();

  // https://github.com/sveltejs/svelte/issues/5604
  const hasPrependSlot = prepend;
  const hasAppendSlot = append;
  const hasCustomContentSlot = itemContent;

  run(() => {
    if (sort) {
      choices = choices.sort((a, b) =>
        a.label.localeCompare(b.label, "fr", { numeric: true })
      );
    }
  });

  const prepend_render = $derived(prepend);
  const itemContent_render = $derived(itemContent);
  const append_render = $derived(append);
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
  className="rounded-sm focus-within:shadow-focus {extraClass}"
  inputClassName="focus:outline-hidden border rounded-sm border-gray-03"
  dropdownClassName="top-[48px]! rounded-sm shadow-md"
  showLoadingIndicator
  {hideArrow}
  {showClear}
  {hasPrependSlot}
  {hasAppendSlot}
  {hasCustomContentSlot}
  {errorMessages}
>
  {#snippet prepend()}
    {@render prepend_render?.()}
  {/snippet}

  {#snippet itemContent({ item })}
  
      {@render itemContent_render?.({ item, })}
    
  {/snippet}

  {#snippet append()}
    {@render append_render?.()}
  {/snippet}
</AutoComplete>
