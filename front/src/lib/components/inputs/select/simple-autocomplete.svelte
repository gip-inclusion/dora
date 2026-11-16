<!--
  Initialy forked from
  https://github.com/pstanoev/simple-svelte-autocomplete/blob/2de0d7618b37192ec1ca47bbe4ffd47477b38792/src/SimpleAutocomplete.svelte
-->
<script lang="ts">
  // TODO: lint this file properly
  /* eslint-disable */
  import { onMount, type Snippet } from "svelte";

  import CheckLineSystem from "svelte-remix/CheckLineSystem.svelte";
  import CloseCircleFillSystem from "svelte-remix/CloseCircleFillSystem.svelte";

  import HighlightedText from "#lib/components/display/highlighted-text.svelte";
  import {
    buildHighlightPatterns,
    removeAccents,
    splitHighlight,
  } from "#lib/utils/highlight.ts";

  import CheckboxMark from "#lib/components/display/checkbox-mark.svelte";
  import { clickOutside } from "#lib/utils/misc.ts";
  import { formatErrors } from "#lib/validation/validation.ts";

  // --- Internal State ----
  const uniqueId = `sautocomplete-${Math.floor(Math.random() * 1000)}`;

  interface Props {
    // the list of items the user can select from
    items?: any;
    initialLabels?: Array<{ value: any; label: string }>;
    // a list of items values that the user can not remove (ex: structure national labels)
    fixedItemsValues?: string[];
    // function to use to get all items (alternative to providing items)
    searchFunction?: (searchText: string) => Promise<any[]>;
    textCleanFunction?: any;
    // events
    onblur?: (evt: FocusEvent) => void;
    onChange?: any;
    onFocus?: any;
    // Behaviour properties
    selectFirstIfEmpty?: boolean;
    minCharactersToSearch?: number;
    maxItemsToShowInList?: number;
    multiple?: boolean;
    // ignores the accents when matching items
    ignoreAccents?: boolean;
    // all the input keywords should be matched in the item keywords
    matchAllKeywords?: boolean;
    // sorts the items by the number of matching keywords
    sortByMatchedKeywords?: boolean;
    // allow users to use a custom item filter function
    itemFilterFunction?: any;
    // allow users to use a custom item sort function
    itemSortFunction?: any;
    // do not allow re-selection after initial selection
    lock?: boolean;
    // delay to wait after a keypress to search for new items
    delay?: number;
    // true to perform local filtering of items, even if searchFunction is provided
    localFiltering?: boolean;

    // UI properties

    // option to hide the dropdown arrow
    hideArrow?: boolean;
    // option to show clear selection button
    showClear?: boolean;
    // option to show loading indicator when the async function is executed
    showLoadingIndicator?: boolean;
    // text displayed when no items match the input text
    noResultsText?: string;
    // text displayed when async data is being loaded
    loadingText?: string;
    // the text displayed when no option is selected
    placeholder?: string;
    // the text displayed when at least one option is selected
    placeholderMulti?: string;
    // apply a className to the control
    className?: string;

    // HTML input UI properties

    // apply a className to the input control
    inputClassName?: string;
    // apply a id to the input control
    inputId: string;
    // generate an HTML input with this name
    name?: any;
    // generate a <select> tag that holds the value
    selectName?: any;
    // apply a id to the <select>
    selectId?: any;
    // add the title to the HTML input
    title?: any;
    // enable the html5 autocompletion to the HTML input
    html5autocomplete?: boolean;
    // make the input readonly
    readonly?: boolean;
    // apply a className to the dropdown div
    dropdownClassName?: string;
    // adds the disabled tag to the HTML input and tag deletion
    disabled?: boolean;
    errorMessages?: string[];

    // --- Public State ----

    // selected item state
    value?: any;
    initialValue?: any;

    text?: string;
    prepend?: Snippet;
    itemContent?: Snippet<[any]>;
    append?: Snippet;
  }

  let {
    items = $bindable([]),
    initialLabels = [],
    fixedItemsValues = [],
    searchFunction,
    textCleanFunction = function (userEnteredText) {
      return userEnteredText;
    },
    onblur,
    onChange = function (_newValue) {},
    onFocus = function () {},
    selectFirstIfEmpty = false,
    minCharactersToSearch = 1,
    maxItemsToShowInList = 0,
    multiple = false,
    ignoreAccents = true,
    matchAllKeywords = true,
    sortByMatchedKeywords = false,
    itemFilterFunction,
    itemSortFunction,
    lock = false,
    delay = 0,
    localFiltering = true,
    hideArrow = false,
    showClear = true,
    showLoadingIndicator = false,
    noResultsText = "Aucun résultat",
    loadingText = "Chargement des résultats…",
    placeholder = "",
    placeholderMulti = "",
    className = "",
    inputClassName = "",
    inputId,
    name,
    selectName,
    selectId,
    title,
    html5autocomplete = false,
    readonly = false,
    dropdownClassName = "",
    disabled = false,
    errorMessages = [],
    value = $bindable(),
    initialValue,
    text = $bindable(""),
    prepend,
    itemContent,
    append,
  }: Props = $props();

  // HTML elements
  let input: HTMLInputElement | undefined = $state();
  let list: HTMLDivElement | undefined = $state();

  // UI state
  let opened = $state(false);
  let skipOpenOnNextFocus = false;
  let loading = $state(false);

  let highlightIndex = $state(-1);

  let filteredTextLength = 0;

  // view model
  let filteredListItems: any[] = $state([]);

  // requests/responses counters
  let lastRequestId = 0;
  let lastResponseId = 0;

  // other state
  let inputDelayTimeout;
  let showList = $state(false);

  // -- Reactivity --

  // `items` est remplacé à chaque nouvelle recherche : on mémorise le libellé
  // des valeurs sélectionnées pour pouvoir continuer à les afficher ensuite.
  // `initialLabels` amorce ce cache pour les valeurs déjà sélectionnées au
  // chargement, qui ne figurent dans aucun résultat de recherche.
  const selectedLabels = new Map(
    initialLabels.map(({ value, label }) => [value, label])
  );

  function getLabelForValue(val) {
    const item = items.find((i) => i.value === val);
    if (item) {
      selectedLabels.set(val, item.label);
    }
    return item?.label ?? selectedLabels.get(val);
  }

  function isFixedItem(val) {
    const fixedItemValue = fixedItemsValues.find(
      (fixedValue) => fixedValue === val
    );
    return !!fixedItemValue;
  }

  // En sélection multiple, la saisie est vidée après chaque choix. `filteredTextLength`
  // et `items` gardaient sinon la requête précédente : au retour du focus, `open()` les
  // relisait et rouvrait la liste sur des suggestions sans rapport avec un champ vide.
  function resetSearchState() {
    filteredTextLength = 0;
    if (searchFunction) {
      items = [];
      filteredListItems = [];
    } else {
      filteredListItems = listItems;
    }
  }

  function updateValue(newValue) {
    if (newValue) {
      const newText = multiple ? "" : getLabelForValue(newValue);
      if (text !== newText) {
        text = newText;
      }
      if (multiple) {
        resetSearchState();
      }
      value = newValue;
      onChange(newValue);
    } else if (initialValue && text !== initialValue) {
      text = initialValue;
    }
    if (!multiple) {
      close();
    }
  }

  onMount(() => {
    if (value && !text) {
      text = getLabelForValue(value);
    }
  });

  $effect(() => {
    // Si text est vide et qu'on est en sélection simple, on réinitialise la valeur
    if (!multiple && !text) {
      updateValue(undefined);
    }
  });

  let listItems: any[] = $derived(prepareListItems(items));

  let clearable = $derived(showClear && (lock || multiple) && value);

  // --- Functions ---

  function safeKeywordsFunction(item) {
    const keywords = item?.label;
    let result = keywords;
    result = result.toLowerCase().trim();
    if (ignoreAccents) {
      result = removeAccents(result);
    }
    return result;
  }

  function prepareListItems(items: any[]) {
    if (!Array.isArray(items) || items.length === 0) {
      return [];
    }

    let selectableItems;
    if (fixedItemsValues && fixedItemsValues.length > 0) {
      selectableItems = items.filter(
        (item) =>
          !fixedItemsValues.find((fixedValue) => fixedValue === item.value)
      );
    } else {
      selectableItems = items;
    }

    return selectableItems.map(getListItem);
  }

  function getListItem(item) {
    return {
      value: item.value,
      // keywords representation of the item
      keywords: safeKeywordsFunction(item),
      // item label
      label: item.label,
      // store reference to the origial item
      item,
    };
  }

  function prepareUserEnteredText(userEnteredText) {
    if (userEnteredText === undefined || userEnteredText === null) {
      return "";
    }

    const textFiltered = userEnteredText
      .replace(/[&/\\#,+()$~%.'":*?<>{}]/gu, " ")
      .trim();

    filteredTextLength = textFiltered.length;

    if (minCharactersToSearch > 1) {
      if (filteredTextLength < minCharactersToSearch) {
        return "";
      }
    }

    const cleanUserEnteredText = textCleanFunction(textFiltered);
    const textFilteredLowerCase = cleanUserEnteredText.toLowerCase().trim();

    return textFilteredLowerCase;
  }

  function numberOfMatches(listItem, searchWords) {
    if (!listItem) {
      return 0;
    }

    const itemKeywords = listItem.keywords;

    let matches = 0;
    searchWords.forEach((searchWord) => {
      if (itemKeywords.includes(searchWord)) {
        matches++;
      }
    });

    return matches;
  }

  async function search() {
    const textFiltered = prepareUserEnteredText(text);

    if (textFiltered === "") {
      if (searchFunction) {
        // we will need to rerun the search
        items = [];
      } else {
        filteredListItems = listItems;
      }

      return;
    }

    if (!searchFunction) {
      processListItems(textFiltered);
    }

    // external search which provides items
    else {
      lastRequestId += 1;
      const currentRequestId = lastRequestId;
      loading = true;

      // searchFunction is a generator
      if (searchFunction.constructor.name === "AsyncGeneratorFunction") {
        for await (const chunk of await searchFunction(textFiltered)) {
          // a chunk of an old response: throw it away
          if (currentRequestId < lastResponseId) {
            return false;
          }

          // a chunk for a new response: reset the item list
          if (currentRequestId > lastResponseId) {
            items = [];
          }

          lastResponseId = currentRequestId;
          items = [...items, ...chunk];
          processListItems(textFiltered);
        }

        // there was nothing in the chunk
        if (lastResponseId < currentRequestId) {
          lastResponseId = currentRequestId;
          items = [];
          processListItems(textFiltered);
        }
      }

      // searchFunction is a regular function
      else {
        const result = await searchFunction(textFiltered);

        // If a response to a newer request has been received
        // while responses to this request were being loaded,
        // then we can just throw away this outdated results.
        if (currentRequestId < lastResponseId) {
          return false;
        }

        lastResponseId = currentRequestId;
        items = result;
        processListItems(textFiltered);
      }

      loading = false;
    }
  }

  function defaultItemFilterFunction(listItem, searchWords) {
    const matches = numberOfMatches(listItem, searchWords);
    if (matchAllKeywords) {
      return matches >= searchWords.length;
    }
    return matches > 0;
  }

  function defaultItemSortFunction(obj1, obj2, searchWords) {
    return (
      numberOfMatches(obj2, searchWords) - numberOfMatches(obj1, searchWords)
    );
  }

  function processListItems(textFiltered) {
    // cleans, filters, orders, and highlights the list items
    prepareListItems(items);

    // local search
    let tempfilteredListItems;
    if (localFiltering) {
      let searchWords;
      if (textFiltered) {
        searchWords = textFiltered;
        if (ignoreAccents) {
          searchWords = removeAccents(searchWords);
        }
        searchWords = searchWords.split(" ");
      }

      if (itemFilterFunction) {
        tempfilteredListItems = listItems.filter((item) =>
          itemFilterFunction(item, searchWords)
        );
      } else {
        tempfilteredListItems = listItems.filter((item) =>
          defaultItemFilterFunction(item, searchWords)
        );
      }

      if (sortByMatchedKeywords) {
        if (itemSortFunction) {
          tempfilteredListItems = tempfilteredListItems.sort((item1, item2) =>
            itemSortFunction(item1, item2, searchWords)
          );
        } else {
          tempfilteredListItems = tempfilteredListItems.sort((item1, item2) =>
            defaultItemSortFunction(item1, item2, searchWords)
          );
        }
      }
    } else {
      tempfilteredListItems = listItems;
    }

    const hlfilter = highlightFilter(textFiltered, ["label"]);
    const filteredListItemsHighlighted = tempfilteredListItems.map(hlfilter);

    filteredListItems = filteredListItemsHighlighted;

    return true;
  }

  function selectListItem(listItem) {
    const newValue = listItem.value;

    // on mémorise le libellé de l'élément choisi : `items` sera remplacé à la
    // prochaine recherche et on ne pourrait plus l'y retrouver
    selectedLabels.set(newValue, listItem.label);

    // simple selection
    if (!multiple) {
      updateValue(newValue);
    }
    // first selection of multiple ones
    else if (!value) {
      updateValue([newValue]);
    }
    // selecting something already selected => unselect it
    else if (value.includes(newValue)) {
      updateValue(value.filter((i) => i !== newValue));
    }
    // adds the element to the selection
    else {
      updateValue([...value, newValue]);
    }

    return true;
  }

  function selectItem() {
    if (filteredListItems.length && highlightIndex >= 0) {
      const listItem = filteredListItems[highlightIndex];
      if (selectListItem(listItem)) {
        close();
        if (multiple) {
          input?.focus();
        }
      }
    }
  }

  function up() {
    if (highlightIndex > 0) highlightIndex--;
    highlight();
  }

  function down() {
    if (highlightIndex < filteredListItems.length - 1) highlightIndex++;
    highlight();
  }

  function highlight() {
    const query = ".selected";

    const el = list && list.querySelector(query);
    if (el) {
      if (typeof (el as any).scrollIntoViewIfNeeded === "function") {
        (el as any).scrollIntoViewIfNeeded();
      }
    }
  }

  function onListItemClick(listItem) {
    if (selectListItem(listItem)) {
      close();
      if (multiple) {
        input?.focus();
      }
    }
  }

  function onDocumentClick(e) {
    if (e.target.closest(`.${uniqueId}`)) {
      // resetListToAllItemsAndOpen();
      highlight();
    }
  }

  function onKeyDown(e) {
    let key = e.key;
    if (key === "Tab" && e.shiftKey) key = "ShiftTab";
    const fnmap = {
      Tab: opened ? down.bind(this) : null,
      ShiftTab: opened ? up.bind(this) : null,
      ArrowDown: down.bind(this),
      ArrowUp: up.bind(this),
      Escape: onEsc.bind(this),
      Backspace:
        multiple && value && value.length && !text
          ? onBackspace.bind(this)
          : null,
    };
    const fn = fnmap[key];
    if (typeof fn === "function") {
      e.preventDefault();
      fn(e);
    }
  }

  function onKeyPress(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      if (opened) {
        onEnter();
      } else {
        open();
      }
    }
  }

  function onEnter() {
    selectItem();
  }

  function onInput(e) {
    text = e.target.value;
    if (inputDelayTimeout) {
      clearTimeout(inputDelayTimeout);
    }

    if (delay) {
      inputDelayTimeout = setTimeout(processInput, delay);
    } else {
      processInput();
    }
  }

  function unselectItem(tag) {
    if (disabled || readonly) return;

    updateValue(value.filter((i) => i !== tag));
    // On redonne le focus à l'input sans rouvrir la liste déroulante
    skipOpenOnNextFocus = document.activeElement !== input;
    input?.focus();
  }

  async function processInput() {
    await search();
    highlightIndex = 0;
    open();
  }

  function onInputClick() {
    resetListToAllItemsAndOpen();
  }

  function onEsc(e) {
    if (opened) {
      e.stopPropagation();

      input?.focus();
      close();
    }
  }

  function onBackspace(_e) {
    unselectItem(value[value.length - 1]);
  }

  function onFocusInternal() {
    onFocus();

    if (skipOpenOnNextFocus) {
      skipOpenOnNextFocus = false;
      return;
    }

    resetListToAllItemsAndOpen();
  }

  function resetListToAllItemsAndOpen() {
    filteredListItems = listItems;

    // When an async component is initialized, the item list
    // must be loaded when the input is focused.
    if (!listItems.length && value && searchFunction) {
      search();
    }
    open();

    // find selected item
    if (value) {
      for (let i = 0; i < listItems.length; i++) {
        const listItem = listItems[i];
        if (typeof listItem === "undefined") {
          continue;
        }

        if (value === listItem.value) {
          highlightIndex = i;

          highlight();
          break;
        }
      }
    }
  }

  function open() {
    // check if the search text has more than the min chars required
    showList =
      (minCharactersToSearch === 1 ||
        (minCharactersToSearch > 1 &&
          filteredTextLength >= minCharactersToSearch)) &&
      ((items && items.length > 0) || filteredTextLength > 0);

    if (!prepend && !append && !showList) {
      return;
    }

    opened = true;
  }

  function close() {
    opened = false;
    loading = false;

    if (!text && selectFirstIfEmpty) {
      selectItem();
    }
  }

  function clear() {
    updateValue(multiple ? [] : undefined);
    text = "";

    setTimeout(() => {
      input?.focus();
      close();
    });
  }

  function highlightFilter(keywords, fields) {
    const patterns = buildHighlightPatterns(keywords, ignoreAccents);
    return (item) => {
      const newItem = Object.assign({ highlighted: {} }, item);
      if (fields) {
        fields.forEach((field) => {
          if (newItem[field]) {
            newItem.highlighted[field] = splitHighlight(
              newItem[field],
              patterns
            );
          }
        });
      }
      return newItem;
    };
  }
</script>

<div
  class="{className || ''}
  {hideArrow || !items.length ? 'hide-arrow' : ''}
  {multiple ? 'is-multiple' : ''} autocomplete select is-fullwidth {uniqueId}"
  class:show-clear={clearable}
  class:is-loading={showLoadingIndicator && loading}
  {@attach clickOutside(close)}
>
  <select name={selectName} id={selectId}>
    {#if !multiple && value}
      <option {value} selected>{text}</option>
    {:else if multiple && value}
      {#each value as i}
        <option value={i} selected>
          {getLabelForValue(i)}
        </option>
      {/each}
    {/if}
  </select>

  <div class="input-container">
    <input
      type="text"
      class="{inputClassName ||
        ''} input autocomplete-input read-only:text-gray-03 disabled:bg-gray-00"
      id={inputId}
      autocomplete={html5autocomplete ? "on" : "off"}
      placeholder={multiple && value.length ? placeholderMulti : placeholder}
      {name}
      {disabled}
      {title}
      readonly={readonly || (lock && value)}
      bind:this={input}
      bind:value={text}
      oninput={onInput}
      onfocus={onFocusInternal}
      {onblur}
      onkeydown={onKeyDown}
      onclick={onInputClick}
      onkeypress={onKeyPress}
      aria-describedby={formatErrors(name, errorMessages)}
    />
    {#if clearable && text?.length}
      <button type="button" onclick={clear} class="autocomplete-clear-button"
        >&#10006;</button
      >
    {/if}
  </div>

  <div
    class="{dropdownClassName || ''} autocomplete-list is-fullwidth"
    class:hidden={!opened}
    bind:this={list}
  >
    {#if prepend}
      {@render prepend()}
      <hr class:hidden={!showList} class="mx-s20" />
    {/if}

    <div class:hidden={!showList} class="py-s10 text-f14">
      {#if filteredListItems && filteredListItems.length > 0}
        {#each filteredListItems as listItem, i}
          {#if listItem && (maxItemsToShowInList <= 0 || i < maxItemsToShowInList)}
            {#if listItem}
              {@const confirmed =
                value &&
                (multiple
                  ? value.includes(listItem.value)
                  : listItem.value === value)}
              <button
                type="button"
                class="autocomplete-list-item px-s20 py-s6 flex w-full flex-row items-baseline text-left {i ===
                highlightIndex
                  ? 'selected'
                  : ''} {multiple ? 'gap-s10' : 'justify-between'}"
                class:confirmed
                onclick={(event: Event) => {
                  event.preventDefault();
                  onListItemClick(listItem);
                }}
                onpointerenter={() => {
                  highlightIndex = i;
                }}
              >
                {#if multiple}
                  <CheckboxMark checked={confirmed} />
                {/if}

                {#if itemContent}
                  {@render itemContent({ item: listItem })}
                {:else}
                  <div>
                    <HighlightedText
                      text={listItem.label}
                      segments={listItem.highlighted?.label}
                    />
                  </div>
                {/if}

                {#if !multiple}
                  <div class="checkmark invisible grow-0">
                    <div class="ml-s8 h-s16 w-s24 fill-current">
                      <CheckLineSystem class="w-s24 h-s16" />
                    </div>
                  </div>
                {/if}
              </button>
            {/if}
          {/if}
        {/each}

        {#if maxItemsToShowInList > 0 && filteredListItems.length > maxItemsToShowInList}
          <div class="autocomplete-list-item-no-results">
            ...{filteredListItems.length - maxItemsToShowInList} results not shown
          </div>
        {/if}
      {:else if loading && loadingText}
        <div class="autocomplete-list-item-loading">
          <span class="text-gray-text-alt">{loadingText}</span>
        </div>
      {:else if noResultsText}
        <div class="autocomplete-list-item-no-results">
          <span class="text-error">{noResultsText}</span>
        </div>
      {/if}
    </div>

    {#if append}
      <hr class:hidden={!showList} class="mx-s20" />
      {@render append()}
    {/if}
  </div>
</div>
{#if multiple && value.length}
  <div class="tags-container">
    {#each value as tagItem}
      <div
        class="tags bg-magenta-brand text-f14 font-bold break-all text-white"
      >
        {getLabelForValue(tagItem)}

        {#if !disabled && !readonly && !isFixedItem(tagItem)}
          <button
            type="button"
            class="tag-delete"
            onclick={(event) => {
              event.preventDefault();
              unselectItem(tagItem);
            }}
          >
            <CloseCircleFillSystem size="16" />
          </button>
        {/if}
      </div>
    {/each}
  </div>
{/if}
<svelte:window onclick={onDocumentClick} />

<style lang="postcss">
  @reference "../../../../app.css";

  .autocomplete {
    position: relative;
    display: inline-block;
    max-width: 100%;
    vertical-align: top;
  }

  .autocomplete:not(.hide-arrow):not(.is-loading)::after {
    position: absolute;
    z-index: 4;
    top: 50%;
    right: 1.125em;
    display: block;
    width: 0.625em;
    height: 0.625em;
    border: 3px solid transparent;
    border-color: #3273dc;
    border-top: 0;
    border-right: 0;
    margin-top: -0.4375em;
    border-radius: 2px;
    content: " ";
    pointer-events: none;
    -webkit-transform: rotate(-45deg);
    transform: rotate(-45deg);
    -webkit-transform-origin: center;
    transform-origin: center;
  }

  .autocomplete.show-clear:not(.hide-arrow)::after {
    right: 2.3em;
  }

  .autocomplete * {
    box-sizing: border-box;
  }

  .autocomplete-input {
    width: 100%;
    height: 100%;
    padding: 12px;
    font: inherit;
  }

  .autocomplete:not(.hide-arrow) .autocomplete-input {
    padding-right: 2em;
  }

  .autocomplete.show-clear:not(.hide-arrow) .autocomplete-input {
    padding-right: 3.2em;
  }

  .autocomplete.hide-arrow.show-clear .autocomplete-input {
    padding-right: 2em;
  }

  .autocomplete-list {
    position: absolute;
    z-index: 99;
    top: 20px;
    width: 100%;
    max-height: calc(15 * (1rem + 10px) + 15px);
    background: #fff;
    overflow-y: auto;
    user-select: none;
  }

  .autocomplete-list-item {
    color: var(--col-text);
    cursor: pointer;
    line-height: 1.25;
  }

  .autocomplete-list-item.confirmed {
    background-color: white;
    color: var(--col-magenta-cta);
  }

  .autocomplete-list-item.confirmed .checkmark {
    visibility: visible;
  }

  .autocomplete-list-item.selected {
    background-color: var(--col-gray-bg);
    color: var(--col-text);
  }

  .autocomplete-list-item.selected.confirmed {
    background-color: var(--col-gray-bg);
    color: var(--col-magenta-cta);
  }

  .autocomplete-list-item-no-results {
    padding: 5px 15px;
    color: #999;
    line-height: 1;
  }

  .autocomplete-list-item-loading {
    padding: 5px 15px;
    line-height: 1;
  }

  .autocomplete-list.hidden {
    display: none;
  }

  .autocomplete.show-clear .autocomplete-clear-button {
    position: absolute;
    z-index: 4;
    top: 50%;
    right: 0.1em;
    display: block;
    padding: 0.3em 0.6em;
    cursor: pointer;
    text-align: center;
    -webkit-transform: translateY(-50%);
    -ms-transform: translateY(-50%);
    transform: translateY(-50%);
  }

  .autocomplete:not(.show-clear) .autocomplete-clear-button {
    display: none;
  }

  .autocomplete select {
    display: none;
  }

  .tags-container {
    @apply mt-s12 gap-s8 flex flex-row flex-wrap;
  }

  .tags {
    display: flex;
    flex-direction: row;
    border-radius: var(--spacing-s4);
    padding: var(--spacing-s2) var(--spacing-s2) var(--spacing-s2)
      var(--spacing-s8);
  }

  .tag-delete {
    position: relative;
    margin-left: 4px;
    cursor: pointer;
    fill: currentColor;
  }
</style>
