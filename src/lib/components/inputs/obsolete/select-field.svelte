<script lang="ts">
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import { arrowDownSIcon, arrowUpSIcon, deleteBackIcon } from "$lib/icons";
  import type { Choice } from "$lib/types";
  import { getChoiceFromValue } from "$lib/utils/choice";
  import { clickOutside } from "$lib/utils/misc";
  import { randomId } from "$lib/utils/random";
  import SelectLabel from "./select-label.svelte";
  import SelectOptions from "./select-options.svelte";

  export let label: string;
  export let name: string;
  export let minDropdownWidth = "min-w-full";
  export let value: string | string[] | undefined;
  export let placeholder = "";
  export let inputMode: "none" | undefined = undefined;
  export let required = false;
  export let isMultiple = false;
  export let withAutoComplete = false;
  export let withClearButton = false;
  export let hideLabel = false;
  export let showIconForSelectedOption = false;
  export let choices: Choice[];
  export let display: "horizontal" | "vertical" = "horizontal";
  export let style: "common" | "filter" | "search" = "common";
  export let onChange: (event: {
    detail: string;
    value: string | string[];
  }) => void | undefined = undefined;

  const originalChoices: Choice[] = [...choices];
  let filterText = "";

  // *** Accessibilité
  const uuid: string = randomId(); // Pour éviter les conflits d'id si le composant est présent plusieurs fois sur la page
  let expanded = false;

  // Gestion de l'outline avec la navigation au clavier
  let selectedOptionIndex: number | null = null;
  let selectedOption: Choice | undefined;

  function toggleCombobox(forceValue?: boolean) {
    expanded = forceValue !== undefined ? forceValue : !expanded;
    if (!expanded) {
      selectedOptionIndex = null;
      selectedOption = null;
    }
  }

  function findChoiceIndex(allChoices: Choice[], val: string) {
    return allChoices.findIndex((choice) => choice.value === val);
  }

  function scrollToOption(id: string) {
    const scrollTop = document.getElementById(id).offsetTop;
    document.getElementById(`listbox-values-${uuid}`).scrollTop =
      scrollTop - 60;
  }

  function updateValue(newValue: string) {
    filterText = "";

    // As array
    if (isMultiple) {
      if (value.includes(newValue)) {
        value = (value as string[]).filter((val) => val !== newValue);
      } else {
        // Gestion du bouton "Tous"
        if (newValue.endsWith("--all")) {
          // Si on décoche toutes les options si on sélectionne "Tous"
          value = value.filter((val) => val.endsWith("--all"));
        } else {
          // Si on décoche "Tous" si on sélectionne une option précise
          value = value.filter((val) => !val.endsWith("--all"));
        }

        value = [...value, newValue];
      }
    } else {
      // As string
      value = newValue;
    }
    if (onChange) {
      onChange({ detail: name, value });
    }
    if (!isMultiple) {
      toggleCombobox(false);
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (["Escape", " ", "Enter", "ArrowDown", "ArrowUp"].includes(event.key)) {
      event.preventDefault();
    }
    if (event.code === "Tab" || event.code === "Escape") {
      toggleCombobox(false);
    }

    if (event.code === "Space") {
      toggleCombobox();
    }

    if (event.code === "Enter") {
      if (!expanded) {
        toggleCombobox(true);
      } else {
        if (selectedOption) {
          updateValue(selectedOption.value);
        }
      }
    }

    if (event.code === "ArrowDown") {
      selectedOptionIndex =
        selectedOptionIndex === null ? 0 : selectedOptionIndex + 1;
      selectedOptionIndex = selectedOptionIndex % choices.length;

      selectedOption = choices[selectedOptionIndex];

      scrollToOption(selectedOption.value);
    }
    if (event.code === "ArrowUp") {
      selectedOptionIndex = selectedOptionIndex
        ? selectedOptionIndex - 1
        : choices.length - 1;
      if (selectedOptionIndex < 0) {
        selectedOptionIndex = choices.length - 1;
      }
      selectedOption = choices[selectedOptionIndex];

      scrollToOption(selectedOption.value);
    }
  }

  function clearAll() {
    value = isMultiple ? [] : undefined;
    choices = [...originalChoices];
    filterText = "";

    onChange({ detail: name, value: "" });
  }

  function setAsSelected(val: string | null) {
    if (!val) {
      selectedOptionIndex = null;
      selectedOption = null;
      return;
    }

    selectedOptionIndex = findChoiceIndex(choices, val);
    selectedOption = choices[selectedOptionIndex];
  }

  $: {
    if (!filterText) {
      choices = [...originalChoices];
    } else {
      setAsSelected(null); // On réinitialise la sélection pour le clavier
      toggleCombobox(true); // On ouvre la liste des résultats
    }
  }
</script>

<FieldWrapper {label} id={name} {required} vertical {hideLabel}>
  <div
    id={name}
    aria-controls={`listbox-values-${uuid}`}
    aria-expanded={expanded}
    aria-haspopup="listbox"
    class="combobox w-full self-start rounded border border-gray-03 bg-white p-s12 font-sans disabled:bg-gray-bg disabled:text-gray-text-alt {display}"
    class:filter-style={style === "filter"}
    class:filter-search={style === "search"}
    class:expanded
    class:has-value={isMultiple ? value.length : value}
    role="combobox"
    tabindex="0"
    aria-label={placeholder}
    on:click={() => toggleCombobox()}
    on:keydown={handleKeydown}
    use:clickOutside
    on:click_outside={() => toggleCombobox(false)}
  >
    <div class="current-value flex cursor-pointer items-center justify-between">
      <div class="w-[90%] overflow-hidden text-ellipsis whitespace-nowrap">
        {#if isMultiple && value.length > 0 && choices?.length}
          {value
            .map((val) => {
              const selectedChoice = choices.find(
                (choice) => choice.value === val
              );
              return selectedChoice.selectedLabel ?? selectedChoice.label;
            })
            .join(", ")}
        {:else if !isMultiple && value}
          <SelectLabel
            useSelectedLabel
            choice={getChoiceFromValue(value, choices)}
            showIcon={showIconForSelectedOption}
          />
        {:else if withAutoComplete}
          <input
            type="text"
            inputmode={inputMode}
            class="absolute top-s0 right-s0 h-full w-full bg-transparent pl-s12"
            bind:value={filterText}
            aria-label={placeholder}
            {placeholder}
          />
        {:else}
          <span class="placeholder text-gray-text-alt">
            {placeholder}
          </span>
        {/if}
      </div>

      <div class="h-s24 w-s24 text-gray-text-alt">
        {#if (isMultiple ? value.length > 0 : !!value) && withClearButton}
          <button class="h-s24 w-s24 fill-current " on:click={clearAll}>
            {@html deleteBackIcon}
          </button>
        {:else}
          <span class="chevron h-s24 w-s24 fill-current">
            {#if expanded}
              {@html arrowUpSIcon}
            {:else}
              {@html arrowDownSIcon}
            {/if}
          </span>
        {/if}
      </div>
    </div>

    <div
      class:hidden={!expanded}
      class="absolute top-[52px] left-s0 z-20 flex max-h-s512 flex-col gap-s10 overflow-y-auto rounded border border-gray-00 bg-white p-s12 shadow-md {minDropdownWidth}"
      role="listbox"
      id={`listbox-values-${uuid}`}
      tabindex="-1"
    >
      <SelectOptions
        {value}
        {isMultiple}
        {selectedOption}
        {choices}
        {setAsSelected}
        {updateValue}
      />
    </div>
  </div>
</FieldWrapper>

<style lang="postcss">
  .selected {
    @apply text-magenta-cta;
  }
  .combobox {
    @apply relative;
  }

  @screen lg {
    .vertical {
      @apply lg:w-3/4;
    }
  }

  /* As search */
  .filter-search {
    @apply absolute border-0 bg-transparent py-s0 px-s12;
  }

  @screen lg {
    .filter-search {
      @apply p-s12;
    }
  }

  .filter-search .chevron {
    @apply !text-gray-dark;
  }
  .filter-search .placeholder {
    @apply !text-gray-text;
  }
  .filter-search :global(.option) {
    @apply !min-h-min p-s8;
  }
  .filter-search .optgroup:hover,
  .filter-search .option:hover,
  .filter-search :global(.hover) {
    @apply !bg-magenta-10 !text-magenta-cta;
  }
  .filter-search.has-value .chevron,
  .filter-search.has-value .placeholder,
  .filter-search.has-value .current-value {
    @apply text-magenta-dark;
  }
  .filter-search :global(.option span.selected) {
    @apply text-magenta-cta;
  }

  .filter-search.has-value .chevron {
    @apply bg-magenta-10 text-magenta-cta;
  }

  /* As filter */
  .filter-style {
    @apply rounded-xl px-s16 py-s12;
  }
  .filter-style {
    @apply rounded-xl px-s16 py-s12;
  }
  .filter-style .current-value > div:first-child {
    @apply w-auto;
  }
  .filter-style.combobox {
    @apply relative w-fit;
  }
  .filter-style .chevron {
    @apply text-gray-text;
  }
  .filter-style .placeholder,
  .filter-style .current-value {
    @apply font-bold text-gray-text;
  }

  .filter-style.has-value .chevron,
  .filter-style.has-value .placeholder,
  .filter-style.has-value .current-value {
    @apply text-magenta-dark;
  }

  .filter-style:hover {
    @apply bg-magenta-10;
  }
  .filter-style:hover .placeholder,
  .filter-style:hover .current-value {
    @apply text-magenta-hover;
  }
  .filter-style:hover .chevron {
    @apply text-magenta-hover;
  }

  .filter-style.expanded {
    @apply bg-magenta-cta;
  }
  .filter-style.expanded.has-value {
    @apply bg-magenta-dark;
  }
  .filter-style.expanded .placeholder,
  .filter-style.expanded .current-value,
  .filter-style.expanded .chevron {
    @apply text-white;
  }
</style>
