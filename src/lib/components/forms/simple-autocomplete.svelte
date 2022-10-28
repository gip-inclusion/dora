<!--
  Initialy forked from
  https://github.com/pstanoev/simple-svelte-autocomplete/blob/2de0d7618b37192ec1ca47bbe4ffd47477b38792/src/SimpleAutocomplete.svelte
-->
<script>
  // TODO: lint this file properly
  /* eslint-disable */

  import { checkIcon, closeCircleIcon } from "$lib/icons.js";

  // the list of items  the user can select from
  export let items = [];

  // function to use to get all items (alternative to providing items)
  export let searchFunction = false;

  // function which returns a postfix value to display in the list
  export let postfixValueFunction = undefined;

  export let textCleanFunction = function (userEnteredText) {
    return userEnteredText;
  };

  // events

  export let onChange = function (_newValue) {};
  export let onFocus = function () {};

  // Behaviour properties
  export let selectFirstIfEmpty = false;
  export let minCharactersToSearch = 1;
  export let maxItemsToShowInList = 0;
  export let multiple = false;

  export let hasPrependSlot = false;

  // ignores the accents when matching items
  export let ignoreAccents = true;

  // all the input keywords should be matched in the item keywords
  export let matchAllKeywords = true;

  // sorts the items by the number of matching keywords
  export let sortByMatchedKeywords = false;

  // allow users to use a custom item filter function
  export let itemFilterFunction = undefined;

  // allow users to use a custom item sort function
  export let itemSortFunction = undefined;

  // do not allow re-selection after initial selection
  export let lock = false;

  // delay to wait after a keypress to search for new items
  export let delay = 0;

  // true to perform local filtering of items, even if searchFunction is provided
  export let localFiltering = true;

  // UI properties

  // option to hide the dropdown arrow
  export let hideArrow = false;

  // option to show clear selection button
  export let showClear = true;

  // option to show loading indicator when the async function is executed
  export let showLoadingIndicator = false;

  // text displayed when no items match the input text
  export let noResultsText = "Aucun résultat";

  // text displayed when async data is being loaded
  export let loadingText = "Chargement des résultats…";

  // the text displayed when no option is selected
  export let placeholder = undefined;

  // the text displayed when at least one option is selected
  export let placeholderMulti = undefined;

  // apply a className to the control
  export let className = undefined;

  // HTML input UI properties
  // apply a className to the input control
  export let inputClassName = undefined;
  // apply a id to the input control
  export let inputId = undefined;
  // generate an HTML input with this name
  export let name = undefined;
  // generate a <select> tag that holds the value
  export let selectName = undefined;
  // apply a id to the <select>
  export let selectId = undefined;
  // add the title to the HTML input
  export let title = undefined;
  // enable the html5 autocompletion to the HTML input
  export let html5autocomplete = undefined;
  // make the input readonly
  export let readonly = undefined;
  // apply a className to the dropdown div
  export let dropdownClassName = undefined;
  // adds the disabled tag to the HTML input and tag deletion
  export let disabled = false;

  // --- Public State ----

  // selected item state
  export let value = undefined;
  export let initialValue = undefined;

  // --- Internal State ----
  const uniqueId = `sautocomplete-${Math.floor(Math.random() * 1000)}`;

  // HTML elements
  let input;
  let list;

  // UI state
  let opened = false;
  let loading = false;

  let highlightIndex = -1;
  let text;

  let filteredTextLength = 0;

  // view model
  let filteredListItems;
  let listItems = [];

  // requests/responses counters
  let lastRequestId = 0;
  let lastResponseId = 0;

  // other state
  let inputDelayTimeout;
  let showList = false;

  // -- Reactivity --

  function getLabelForValue(val) {
    const item = items.find((i) => i.value === val);
    return item?.label;
  }

  function onValueChanged() {
    if (value !== undefined) {
      if (multiple) {
        text = "";
      } else {
        text = getLabelForValue(value);
      }
      onChange(value);
    } else if (initialValue) {
      text = initialValue;
    }
    if (!multiple) {
      close();
    }
  }

  function onTextChanged() {
    if (!multiple && (text == null || text === "")) {
      value = null;
    }
  }

  $: value, onValueChanged();
  $: text, onTextChanged();
  $: clearable = showClear && (lock || multiple) && value;

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

  function prepareListItems() {
    if (!Array.isArray(items)) {
      items = [];
    }

    const length = items ? items.length : 0;
    listItems = new Array(length);

    if (length > 0) {
      items.forEach((item, i) => {
        const listItem = getListItem(item);
        listItems[i] = listItem;
      });
    }
  }

  function getListItem(item) {
    return {
      value: item.value,
      // keywords representation of the item
      keywords: safeKeywordsFunction(item),
      // item label
      label: item.label,
      tags: item.tags || [],
      // store reference to the origial item
      item,
    };
  }

  $: items, prepareListItems();

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

      const AsyncGenerator = async function* () {}.constructor;

      // searchFunction is a generator
      if (searchFunction instanceof AsyncGenerator) {
        for await (const chunk of searchFunction(textFiltered)) {
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
    prepareListItems();

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

  function selectListItem(newValue) {
    // simple selection
    if (!multiple) {
      value = newValue;
    }
    // first selection of multiple ones
    else if (!value) {
      value = [newValue];
    }
    // selecting something already selected => unselect it
    else if (value.includes(newValue)) {
      value = value.filter((i) => i !== newValue);
    }
    // adds the element to the selection
    else {
      value = [...value, newValue];
    }

    return true;
  }

  function selectItem() {
    if (filteredListItems.length && highlightIndex >= 0) {
      const listItem = filteredListItems[highlightIndex];
      if (selectListItem(listItem.value)) {
        close();
        if (multiple) {
          input.focus();
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
      if (typeof el.scrollIntoViewIfNeeded === "function") {
        el.scrollIntoViewIfNeeded();
      }
    }
  }

  function onListItemClick(listItem) {
    if (selectListItem(listItem.value)) {
      close();
      if (multiple) {
        input.focus();
      }
    }
  }

  function onDocumentClick(e) {
    if (e.target.closest(`.${uniqueId}`)) {
      // resetListToAllItemsAndOpen();
      highlight();
    } else {
      close();
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
    if (e.key === "Enter" && opened) {
      e.preventDefault();
      onEnter();
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

    value = value.filter((i) => i !== tag);
    input.focus();
  }

  function processInput() {
    if (search()) {
      highlightIndex = 0;
      open();
    }
  }

  function onInputClick() {
    resetListToAllItemsAndOpen();
  }

  function onEsc(e) {
    if (text) return clear();
    e.stopPropagation();
    if (opened) {
      input.focus();
      close();
    }
  }

  function onBackspace(_e) {
    unselectItem(value[value.length - 1]);
  }

  function onFocusInternal() {
    onFocus();

    resetListToAllItemsAndOpen();
  }

  function resetListToAllItemsAndOpen() {
    filteredListItems = listItems;

    // When an async component is initialized, the item list
    // must be loaded when the input is focused.
    if (!listItems.length && value && searchFunction) {
      search();
      closeIfNoList();
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

    if (!hasPrependSlot && !showList) {
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

  function closeIfNoList() {
    if (!hasPrependSlot && !showList) {
      close();
    }
  }

  function clear() {
    value = multiple ? [] : null;
    text = "";

    setTimeout(() => {
      input.focus();
      close();
    });
  }

  export function highlightFilter(keywords, fields) {
    keywords = keywords.split(/\s+/gu);
    return (item) => {
      const newItem = Object.assign({ highlighted: {} }, item);
      if (fields) {
        fields.forEach((field) => {
          if (newItem[field] && !newItem.highlighted[field]) {
            newItem.highlighted[field] = newItem[field];
          }
          if (newItem.highlighted[field]) {
            keywords.forEach((keyword) => {
              const keywordPattern = ignoreAccents
                ? makeAccentInsensitivePattern(removeAccents(keyword))
                : keyword;
              const reg = new RegExp(`(${keywordPattern})`, "igu");
              newItem.highlighted[field] = newItem.highlighted[field].replace(
                reg,
                "<b>$1</b>"
              );
            });
          }
        });
      }
      return newItem;
    };
  }

  function removeAccents(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/gu, "");
  }

  /**
   * Creates a RegExp that matches the words in the search string.
   * Case and accent insensitive @param search_string
   * @param searchString
   *.
   */
  function makeAccentInsensitivePattern(searchString) {
    const accented = {
      A: "[Aa\xaa\xc0-\xc5\xe0-\xe5\u0100-\u0105\u01cd\u01ce\u0200-\u0203\u0226\u0227\u1d2c\u1d43\u1e00\u1e01\u1e9a\u1ea0-\u1ea3\u2090\u2100\u2101\u213b\u249c\u24b6\u24d0\u3371-\u3374\u3380-\u3384\u3388\u3389\u33a9-\u33af\u33c2\u33ca\u33df\u33ff\uff21\uff41]",
      B: "[Bb\u1d2e\u1d47\u1e02-\u1e07\u212c\u249d\u24b7\u24d1\u3374\u3385-\u3387\u33c3\u33c8\u33d4\u33dd\uff22\uff42]",
      C: "[Cc\xc7\xe7\u0106-\u010d\u1d9c\u2100\u2102\u2103\u2105\u2106\u212d\u216d\u217d\u249e\u24b8\u24d2\u3376\u3388\u3389\u339d\u33a0\u33a4\u33c4-\u33c7\uff23\uff43]",
      D: "[Dd\u010e\u010f\u01c4-\u01c6\u01f1-\u01f3\u1d30\u1d48\u1e0a-\u1e13\u2145\u2146\u216e\u217e\u249f\u24b9\u24d3\u32cf\u3372\u3377-\u3379\u3397\u33ad-\u33af\u33c5\u33c8\uff24\uff44]",
      E: "[Ee\xc8-\xcb\xe8-\xeb\u0112-\u011b\u0204-\u0207\u0228\u0229\u1d31\u1d49\u1e18-\u1e1b\u1eb8-\u1ebd\u2091\u2121\u212f\u2130\u2147\u24a0\u24ba\u24d4\u3250\u32cd\u32ce\uff25\uff45]",
      F: "[Ff\u1da0\u1e1e\u1e1f\u2109\u2131\u213b\u24a1\u24bb\u24d5\u338a-\u338c\u3399\ufb00-\ufb04\uff26\uff46]",
      G: "[Gg\u011c-\u0123\u01e6\u01e7\u01f4\u01f5\u1d33\u1d4d\u1e20\u1e21\u210a\u24a2\u24bc\u24d6\u32cc\u32cd\u3387\u338d-\u338f\u3393\u33ac\u33c6\u33c9\u33d2\u33ff\uff27\uff47]",
      H: "[Hh\u0124\u0125\u021e\u021f\u02b0\u1d34\u1e22-\u1e2b\u1e96\u210b-\u210e\u24a3\u24bd\u24d7\u32cc\u3371\u3390-\u3394\u33ca\u33cb\u33d7\uff28\uff48]",
      I: "[Ii\xcc-\xcf\xec-\xef\u0128-\u0130\u0132\u0133\u01cf\u01d0\u0208-\u020b\u1d35\u1d62\u1e2c\u1e2d\u1ec8-\u1ecb\u2071\u2110\u2111\u2139\u2148\u2160-\u2163\u2165-\u2168\u216a\u216b\u2170-\u2173\u2175-\u2178\u217a\u217b\u24a4\u24be\u24d8\u337a\u33cc\u33d5\ufb01\ufb03\uff29\uff49]",
      J: "[Jj\u0132-\u0135\u01c7-\u01cc\u01f0\u02b2\u1d36\u2149\u24a5\u24bf\u24d9\u2c7c\uff2a\uff4a]",
      K: "[Kk\u0136\u0137\u01e8\u01e9\u1d37\u1d4f\u1e30-\u1e35\u212a\u24a6\u24c0\u24da\u3384\u3385\u3389\u338f\u3391\u3398\u339e\u33a2\u33a6\u33aa\u33b8\u33be\u33c0\u33c6\u33cd-\u33cf\uff2b\uff4b]",
      L: "[Ll\u0139-\u0140\u01c7-\u01c9\u02e1\u1d38\u1e36\u1e37\u1e3a-\u1e3d\u2112\u2113\u2121\u216c\u217c\u24a7\u24c1\u24db\u32cf\u3388\u3389\u33d0-\u33d3\u33d5\u33d6\u33ff\ufb02\ufb04\uff2c\uff4c]",
      M: "[Mm\u1d39\u1d50\u1e3e-\u1e43\u2120\u2122\u2133\u216f\u217f\u24a8\u24c2\u24dc\u3377-\u3379\u3383\u3386\u338e\u3392\u3396\u3399-\u33a8\u33ab\u33b3\u33b7\u33b9\u33bd\u33bf\u33c1\u33c2\u33ce\u33d0\u33d4-\u33d6\u33d8\u33d9\u33de\u33df\uff2d\uff4d]",
      N: "[Nn\xd1\xf1\u0143-\u0149\u01ca-\u01cc\u01f8\u01f9\u1d3a\u1e44-\u1e4b\u207f\u2115\u2116\u24a9\u24c3\u24dd\u3381\u338b\u339a\u33b1\u33b5\u33bb\u33cc\u33d1\uff2e\uff4e]",
      O: "[Oo\xba\xd2-\xd6\xf2-\xf6\u014c-\u0151\u01a0\u01a1\u01d1\u01d2\u01ea\u01eb\u020c-\u020f\u022e\u022f\u1d3c\u1d52\u1ecc-\u1ecf\u2092\u2105\u2116\u2134\u24aa\u24c4\u24de\u3375\u33c7\u33d2\u33d6\uff2f\uff4f]",
      P: "[Pp\u1d3e\u1d56\u1e54-\u1e57\u2119\u24ab\u24c5\u24df\u3250\u3371\u3376\u3380\u338a\u33a9-\u33ac\u33b0\u33b4\u33ba\u33cb\u33d7-\u33da\uff30\uff50]",
      Q: "[Qq\u211a\u24ac\u24c6\u24e0\u33c3\uff31\uff51]",
      R: "[Rr\u0154-\u0159\u0210-\u0213\u02b3\u1d3f\u1d63\u1e58-\u1e5b\u1e5e\u1e5f\u20a8\u211b-\u211d\u24ad\u24c7\u24e1\u32cd\u3374\u33ad-\u33af\u33da\u33db\uff32\uff52]",
      S: "[Ss\u015a-\u0161\u017f\u0218\u0219\u02e2\u1e60-\u1e63\u20a8\u2101\u2120\u24ae\u24c8\u24e2\u33a7\u33a8\u33ae-\u33b3\u33db\u33dc\ufb06\uff33\uff53]",
      T: "[Tt\u0162-\u0165\u021a\u021b\u1d40\u1d57\u1e6a-\u1e71\u1e97\u2121\u2122\u24af\u24c9\u24e3\u3250\u32cf\u3394\u33cf\ufb05\ufb06\uff34\uff54]",
      U: "[Uu\xd9-\xdc\xf9-\xfc\u0168-\u0173\u01af\u01b0\u01d3\u01d4\u0214-\u0217\u1d41\u1d58\u1d64\u1e72-\u1e77\u1ee4-\u1ee7\u2106\u24b0\u24ca\u24e4\u3373\u337a\uff35\uff55]",
      V: "[Vv\u1d5b\u1d65\u1e7c-\u1e7f\u2163-\u2167\u2173-\u2177\u24b1\u24cb\u24e5\u2c7d\u32ce\u3375\u33b4-\u33b9\u33dc\u33de\uff36\uff56]",
      W: "[Ww\u0174\u0175\u02b7\u1d42\u1e80-\u1e89\u1e98\u24b2\u24cc\u24e6\u33ba-\u33bf\u33dd\uff37\uff57]",
      X: "[Xx\u02e3\u1e8a-\u1e8d\u2093\u213b\u2168-\u216b\u2178-\u217b\u24b3\u24cd\u24e7\u33d3\uff38\uff58]",
      Y: "[Yy\xdd\xfd\xff\u0176-\u0178\u0232\u0233\u02b8\u1e8e\u1e8f\u1e99\u1ef2-\u1ef9\u24b4\u24ce\u24e8\u33c9\uff39\uff59]",
      Z: "[Zz\u0179-\u017e\u01f1-\u01f3\u1dbb\u1e90-\u1e95\u2124\u2128\u24b5\u24cf\u24e9\u3390-\u3394\uff3a\uff5a]",
    };

    // escape meta characters
    searchString = searchString.replace(/([|()[{.+*?^$\\])/gu, "\\$1");

    // split into words
    const words = searchString.split(/\s+/u);

    // sort by length
    const lengthComp = function (a, b) {
      return b.length - a.length;
    };
    words.sort(lengthComp);

    // replace characters by their compositors
    const accentReplacer = function (chr) {
      return accented[chr.toUpperCase()] || chr;
    };
    for (let i = 0; i < words.length; i++) {
      words[i] = words[i].replace(/\S/gu, accentReplacer);
    }

    // join as alternatives
    const regexp = words.join("|");
    return regexp;
  }

  // workaround for
  // ValidationError: 'multiple' attribute cannot be dynamic if select uses two-way binding
  function multipleAction(node) {
    node.multiple = multiple;
  }

  function isConfirmed(newValue) {
    if (!value) {
      return false;
    }
    if (multiple) {
      return value.includes(newValue);
    }
    return newValue === value;
  }
</script>

<div
  class="{className || ''}
  {hideArrow || !items.length ? 'hide-arrow' : ''}
  {multiple ? 'is-multiple' : ''} autocomplete select is-fullwidth {uniqueId}"
  class:show-clear={clearable}
  class:is-loading={showLoadingIndicator && loading}
>
  <select name={selectName} id={selectId} bind:value use:multipleAction>
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
      class="{inputClassName || ''} input autocomplete-input"
      id={inputId}
      autocomplete={html5autocomplete ? "on" : "off"}
      placeholder={multiple && value.length ? placeholderMulti : placeholder}
      {name}
      {disabled}
      {title}
      readonly={readonly || (lock && value)}
      bind:this={input}
      bind:value={text}
      on:input={onInput}
      on:focus={onFocusInternal}
      on:blur
      on:keydown={onKeyDown}
      on:click={onInputClick}
      on:keypress={onKeyPress}
    />
    {#if clearable && text?.length}
      <span on:click={clear} class="autocomplete-clear-button">&#10006;</span>
    {/if}
  </div>

  <div
    class="{dropdownClassName || ''} autocomplete-list is-fullwidth"
    class:hidden={!opened}
    bind:this={list}
  >
    <slot name="prepend" />

    <div class:hidden={!showList} class="py-s10">
      {#if filteredListItems && filteredListItems.length > 0}
        {#each filteredListItems as listItem, i}
          {#if listItem && (maxItemsToShowInList <= 0 || i < maxItemsToShowInList)}
            {#if listItem}
              <div
                class="autocomplete-list-item {i === highlightIndex
                  ? 'selected'
                  : ''}"
                class:confirmed={isConfirmed(listItem.value)}
                on:click={() => onListItemClick(listItem)}
                on:pointerenter={() => {
                  highlightIndex = i;
                }}
              >
                <div class="flex flex-row">
                  <div class="flex grow justify-between">
                    <div>
                      {@html listItem.highlighted
                        ? listItem.highlighted.label
                        : listItem.label}
                    </div>
                    <div class="flex shrink-0 items-baseline">
                      {#each listItem.tags as tag}
                        <div
                          class="break-word shrink-0 rounded bg-gray-01 px-s6 py-s2 text-f12 font-bold text-gray-text"
                        >
                          {tag}
                        </div>
                      {/each}
                      {#if postfixValueFunction}
                        <div
                          class="ml-s8 inline-block text-f12 text-gray-text-alt"
                        >
                          {postfixValueFunction(listItem.value)}
                        </div>
                      {/if}

                      <div class="checkmark hidden grow-0">
                        <div class="ml-s8 h-s16 w-s24 fill-current">
                          {@html checkIcon}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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
  </div>
</div>
{#if multiple && value}
  <div class="tags-container mb-s8">
    {#each value as tagItem}
      <div
        class="tags break-all bg-magenta-brand text-f14 font-bold text-white"
      >
        {getLabelForValue(tagItem)}

        {#if !disabled && !readonly}
          <span
            class="tag-delete"
            on:click|preventDefault={unselectItem(tagItem)}
          >
            {@html closeCircleIcon}
          </span>
        {/if}
      </div>
    {/each}
  </div>
{/if}
<svelte:window on:click={onDocumentClick} />

<style lang="postcss">
  input {
    @apply read-only:text-gray-03 disabled:bg-gray-00;
  }

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
    padding: 6px 15px;
    color: var(--col-text-alt);
    cursor: pointer;
    line-height: 1.25;
  }

  .autocomplete-list-item.confirmed {
    background-color: white;
    color: var(--col-magenta-cta);
  }

  .autocomplete-list-item.confirmed .checkmark {
    display: block;
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
    display: flex;
    margin-top: var(--s16);
    flex-direction: row;
    flex-wrap: wrap;
    gap: var(--s8);
  }

  .tags {
    display: flex;
    flex-direction: row;
    border-radius: var(--s4);
    padding: var(--s2) var(--s8);
  }

  .tag-delete {
    position: relative;
    top: 2px;
    margin-left: 4px;
    cursor: pointer;
    fill: currentColor;
    width: var(--s16);
    height: var(--s16);
    flex-shrink: 0;
  }
</style>
