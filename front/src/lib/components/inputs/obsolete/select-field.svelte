<script lang="ts">
  import ArrowDownSIcon from "svelte-remix/ArrowDownSLineArrows.svelte";
  import ArrowUpSIcon from "svelte-remix/ArrowUpSLineArrows.svelte";
  import DeleteBack2FillSystem from "svelte-remix/DeleteBack2FillSystem.svelte";

  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import type { Choice } from "$lib/types";
  import { getChoiceFromValue } from "$lib/utils/choice";
  import { clickOutside } from "$lib/utils/misc";
  import { randomId } from "$lib/utils/random";

  import SelectLabel from "./select-label.svelte";
  import SelectOptions from "./select-options.svelte";

  interface Props {
    label: string;
    name: string;
    minDropdownWidth?: string;
    value?: string | string[];
    placeholder?: string;
    inputMode?: "none";
    required?: boolean;
    isMultiple?: boolean;
    withAutoComplete?: boolean;
    withClearButton?: boolean;
    hideLabel?: boolean;
    showIconForSelectedOption?: boolean;
    choices: Choice[];
    display?: "horizontal" | "vertical";
    style?: "common" | "filter" | "search";
    onChange?: (event: { detail: string; value: string | string[] }) => void;
    disabled?: boolean;
  }

  let {
    label,
    name,
    minDropdownWidth = "min-w-full",
    value = $bindable(),
    placeholder = "",
    inputMode,
    required = false,
    isMultiple = false,
    withAutoComplete = false,
    withClearButton = false,
    hideLabel = false,
    showIconForSelectedOption = false,
    choices = $bindable(),
    display = "horizontal",
    style = "common",
    onChange,
    disabled = false,
  }: Props = $props();

  const originalChoices: Choice[] = [...choices];
  let filterText = $state("");

  // *** Accessibilité
  const uuid: string = randomId(); // Pour éviter les conflits d'id si le composant est présent plusieurs fois sur la page
  let expanded = $state(false);

  // Gestion de l'outline avec la navigation au clavier
  let selectedOptionIndex: number | null = null;
  let selectedOption: Choice | undefined = $state();

  let hasSelectAllOption = $derived(
    choices.some((choice) => choice.value.endsWith("--all"))
  );

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
        // Désélection d'une option
        value = (value as string[]).filter((val) => val !== newValue);
      } else {
        // Sélection d'une option
        if (hasSelectAllOption) {
          // Il existe une option "Tous"
          if (
            newValue.endsWith("--all") ||
            value?.length === choices.length - 2
          ) {
            // Sélection de l'option "Tous" ou de toutes les options ordinaires
            // => on sélectionne l'option "Tous" et désélectionne toutes les autres
            value = choices
              .filter((choice) => choice.value.endsWith("--all"))
              .map((choice) => choice.value);
          } else {
            // Sélection d'une option ordinaire (sans qu'elles soient toutes sélectionnées)
            // => on désélectionne l'option Tous
            value = value
              .filter((val) => !val.endsWith("--all"))
              .concat([newValue]);
          }
        } else {
          // Il n'y a pas d'option "Tous"
          value = [...value, newValue];
        }
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

  $effect(() => {
    if (!filterText) {
      choices = [...originalChoices];
    } else {
      setAsSelected(null); // On réinitialise la sélection pour le clavier
      toggleCombobox(true); // On ouvre la liste des résultats
    }
  });
</script>

<FieldWrapper {label} id={name} {required} vertical {hideLabel}>
  <div
    id={name}
    aria-controls={`listbox-values-${uuid}`}
    aria-expanded={expanded}
    aria-haspopup="listbox"
    class="combobox border-gray-03 p-s12 disabled:bg-gray-bg disabled:text-gray-text-alt w-full self-start rounded-sm border bg-white font-sans {display}"
    class:filter-style={style === "filter"}
    class:filter-search={style === "search"}
    class:expanded
    class:has-value={isMultiple ? value.length : value}
    class:disabled
    role="combobox"
    tabindex={disabled ? "-1" : "0"}
    aria-label={placeholder}
    aria-disabled={disabled}
    onclick={() => toggleCombobox()}
    onkeydown={handleKeydown}
    {@attach clickOutside(() => toggleCombobox(false))}
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
            class="right-s0 top-s0 pl-s12 absolute h-full w-full bg-transparent"
            bind:value={filterText}
            aria-label={placeholder}
            {placeholder}
            {disabled}
          />
        {:else}
          <span class="placeholder text-gray-text-alt">
            {placeholder}
          </span>
        {/if}
      </div>

      <div class="h-s24 w-s24 text-gray-text-alt">
        {#if (isMultiple ? value.length > 0 : !!value) && withClearButton}
          <button
            class="h-s24 w-s24 fill-current"
            onclick={clearAll}
            {disabled}
          >
            <DeleteBack2FillSystem />
          </button>
        {:else}
          <span class="chevron h-s24 w-s24 fill-current">
            {#if expanded}
              <ArrowUpSIcon />
            {:else}
              <ArrowDownSIcon />
            {/if}
          </span>
        {/if}
      </div>
    </div>

    <div
      class:hidden={!expanded}
      class="left-s0 max-h-s512 border-gray-00 p-s12 absolute top-[52px] z-20 flex flex-col overflow-y-auto rounded-sm border bg-white shadow-md {minDropdownWidth}"
      class:gap-s10={!isMultiple}
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
  @reference "../../../../app.css";

  .selected {
    @apply text-magenta-cta;
  }
  :global(.hover) {
    background-color: var(--color-magenta-10) !important;
    color: var(--color-magenta-cta) !important;
  }
  .combobox {
    @apply relative;
  }

  .combobox.disabled {
    cursor: not-allowed;
    pointer-events: none;
  }

  @media (width >= 64rem) {
    .vertical {
      width: 75%;
    }
  }

  /* As search */
  .filter-search {
    @apply px-s12 py-s0 absolute border-0 bg-transparent;
  }

  @media (width >= 64rem) {
    .filter-search {
      padding: var(--spacing-s12);
    }
  }

  .filter-search .chevron {
    color: var(--color-gray-dark) !important;
  }
  .filter-search .placeholder {
    color: var(--color-gray-text) !important;
  }
  .filter-search :global(.option) {
    padding: var(--spacing-s8) !important;
    min-height: min-content !important;
  }
  .filter-search .optgroup:hover,
  .filter-search .option:hover,
  .filter-search :global(.hover) {
    background-color: var(--color-magenta-10) !important;
    color: var(--color-magenta-cta) !important;
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

  .filter-search.disabled .chevron {
    opacity: 0.3;
  }

  .filter-search.disabled .placeholder {
    opacity: 0.6;
  }

  .filter-search.disabled .current-value {
    opacity: 0.6;
  }

  /* As filter */
  .filter-style {
    @apply px-s16 py-s12 rounded-3xl;
  }
  .filter-style {
    @apply px-s16 py-s12 rounded-3xl;
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
    @apply text-gray-text font-bold;
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
  .filter-style .option:hover,
  .filter-style :global(.hover) {
    background-color: var(--color-magenta-10) !important;
    color: var(--color-magenta-cta) !important;
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
