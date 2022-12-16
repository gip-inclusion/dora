<script lang="ts">
  import { clickOutside } from "$lib/utils/click-outside";
  import { arrowDownSIcon, arrowUpSIcon, deleteBackIcon } from "$lib/icons";
  import type { Choice } from "$lib/types";
  import {
    getCategoryKeyFromSubcategoryChoice,
    getChoiceFromValue,
    getChoicesFromKey,
  } from "$lib/utils/choice";
  import { tick } from "svelte";
  import FieldWrapper from "./field-wrapper.svelte";
  import SelectLabel from "./select-label.svelte";
  import SelectOptions from "./select-options.svelte";

  export let label: string;
  export let name: string;
  export let minDropdownWidth = "min-w-full";
  export let value: string | string[];
  export let placeholder = "";
  export let helper = "";
  export let required = false;
  export let isMultiple = false;
  export let withAutoComplete = false;
  export let withClearButton = false;
  export let hideLabel = false;
  export let showIconForSelectedOption = false;
  export let choices: Choice[];
  export let optGroups: Choice[] = [];
  export let display: "horizontal" | "vertical" = "horizontal";
  export let style: "common" | "filter" | "search" = "common";
  export let errorMessages: string[] | undefined = undefined;
  export let onChange: (event: {
    detail: string;
    value: string | string[];
  }) => void | undefined = undefined;

  const originalChoices: Choice[] = [...choices];
  const originalOptGroups: Choice[] = [...optGroups];

  let optGroupsOpen: string[] = [];

  function optGroupHasSubValuesSelected(optGroup) {
    return value.filter((v) => v.split("--")[0] === optGroup.value).length > 0;
  }

  // AriaDescribedBy => TODO: move to wrapper
  let ariaDescribedBy = "";
  $: {
    ariaDescribedBy = helper ? `${name}-helper` : "";
    if ((errorMessages || []).length) {
      ariaDescribedBy = `${ariaDescribedBy} ${name}-error`;
    }
  }

  // *** Accessibilité
  const uuid: string = crypto.randomUUID(); // Pour éviter les conflits d'id si le composant est présent plusieurs fois sur la page
  let expanded = false;

  // Gestion de l'outline avec la navigation au clavier
  let selectedOptionIndex: number | null = null;
  let selectedOption: Choice | undefined;

  function handleKeydown(event: KeyboardEvent) {
    if (["Escape", " ", "Enter", "ArrowDown", "ArrowUp"].includes(event.key)) {
      event.preventDefault();
    }
    if (event.code === "Tab" || event.code === "Escape") toggleCombobox(false);

    if (event.code === "Space") toggleCombobox();

    if (event.code === "Enter") {
      if (!expanded) {
        toggleCombobox(true);
      } else {
        if (selectedOption) {
          updateValue(selectedOption.value, selectedOption.optGroupKey);
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
      if (selectedOptionIndex < 0) selectedOptionIndex = choices.length - 1;
      selectedOption = choices[selectedOptionIndex];

      scrollToOption(selectedOption.value);
    }
  }

  async function scrollToOption(id: string) {
    // Open if needed
    if (optGroups.length) {
      const key = getCategoryKeyFromSubcategoryChoice(selectedOption);
      if (!optGroupsOpen.includes(key)) {
        optGroupsOpen = [...optGroupsOpen, key];
      }
    }

    await tick();

    const scrollTop = document.getElementById(id).offsetTop;
    document.getElementById(`listbox-values-${uuid}`).scrollTop =
      scrollTop - 60;
  }

  function clearAll() {
    value = isMultiple ? [] : undefined;
    choices = [...originalChoices];
    optGroups = [...originalOptGroups];
    filterText = "";
    if (optGroups) {
      optGroupsOpen = [];
    }
  }

  function updateValue(newValue: string, optGroup: string | undefined) {
    filterText = "";

    // As array
    if (isMultiple) {
      if (value.includes(newValue)) {
        value = (value as string[]).filter((v) => v !== newValue);
      } else {
        // Gestion du bouton "Tous"
        if (optGroups) {
          if (newValue.endsWith("--all")) {
            // Si on décoche toutes les options si on sélectionne "Tous"
            value = value.filter((v) => !v.startsWith(`${optGroup}--`));
          } else {
            // Si on décoche "Tous" si on sélectionne une option précise
            value = value.filter((v) => v !== `${optGroup}--all`);
          }
        }

        value = [...value, newValue];
      }
    } else {
      // As string
      value = newValue;
    }
    if (onChange) onChange({ detail: name, value });
    if (!isMultiple) toggleCombobox(false);
  }

  function toggleCombobox(forceValue?: boolean) {
    expanded = forceValue !== undefined ? forceValue : !expanded;
    if (!expanded) {
      selectedOptionIndex = null;
      selectedOption = null;
    }
  }

  function setAsSelected(value: string | null) {
    if (!value) {
      selectedOptionIndex = null;
      selectedOption = null;
      return;
    }

    selectedOptionIndex = findChoiceIndex(choices, value);
    selectedOption = choices[selectedOptionIndex];
  }

  function findChoiceIndex(choices: Choice[], value: string) {
    return choices.findIndex((c) => c.value === value);
  }

  async function toggleGroup(optGroup: string) {
    if (optGroupsOpen.includes(optGroup)) {
      optGroupsOpen = optGroupsOpen.filter((opt) => opt !== optGroup);
    } else {
      optGroupsOpen = [...optGroupsOpen, optGroup];
    }
  }

  let filterText = "";
  $: {
    if (!filterText) {
      choices = [...originalChoices];
      optGroups = [...originalOptGroups];
      optGroupsOpen = [];
    } else {
      // On filtre les choix et les optGroups
      choices = originalChoices.filter((c) => {
        const optGroupLabel = originalOptGroups.find(
          (g) => g.value === c.optGroupKey
        )?.label;
        return (
          c.label.toLowerCase().includes(filterText.toLocaleLowerCase()) ||
          optGroupLabel.toLowerCase().includes(filterText.toLocaleLowerCase())
        );
      });

      // On réinitialise la sélection pour le clavier
      setAsSelected(null);

      // On ouvre la livre des résultats
      toggleCombobox(true);

      // On filtre et ouvre les optgroup ayant des options
      if (optGroups) {
        const optGroupKeys = new Set<string>();
        choices.forEach((c) => optGroupKeys.add(c.optGroupKey));

        optGroupsOpen = Array.from(optGroupKeys.values());
        optGroups = originalOptGroups.filter((o) => optGroupKeys.has(o.value));
      }
    }
  }
</script>

<FieldWrapper
  {label}
  {name}
  {helper}
  {required}
  {errorMessages}
  {display}
  {hideLabel}
>
  <div
    id={name}
    aria-controls={`listbox-values-${uuid}`}
    aria-expanded={expanded}
    aria-haspopup="listbox"
    aria-labelledby={`button-label-${uuid}`}
    class="combobox w-full self-start rounded border border-gray-03 bg-white p-s12 font-sans disabled:bg-gray-bg disabled:text-gray-text-alt {display}"
    class:filter-style={style === "filter"}
    class:filter-search={style === "search"}
    class:expanded
    class:has-value={isMultiple ? value.length : value}
    role="combobox"
    tabindex="0"
    aria-describedby={ariaDescribedBy}
    on:click={() => toggleCombobox()}
    on:keydown={handleKeydown}
    use:clickOutside
    on:click_outside={() => toggleCombobox(false)}
  >
    <div class="current-value flex cursor-pointer items-center justify-between">
      <div class="w-[90%] overflow-hidden text-ellipsis whitespace-nowrap">
        {#if isMultiple && value.length > 0}
          {value
            .map((v) => {
              const choice = choices.find((c) => c.value === v);
              return choice.selectedLabel ?? choice.label;
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
            class="absolute top-s0 right-s0 h-full w-full bg-transparent pl-s12"
            bind:value={filterText}
            {placeholder}
          />
        {:else}
          <span class="placeholder text-gray-text-alt">{placeholder}</span>
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
      aria-labelledby={`button-label-${uuid}`}
      tabindex="-1"
    >
      {#each optGroups as optGroup (optGroup.value)}
        {@const hasSubValuesSelected = optGroupHasSubValuesSelected(optGroup)}
        {@const open =
          optGroupsOpen.includes(optGroup.value) || hasSubValuesSelected}
        <div class="w-full">
          <button
            class="optgroup flex w-full justify-between p-s12 text-gray-text"
            class:has-sub-value-selected={hasSubValuesSelected}
            on:click|preventDefault|stopPropagation={() =>
              toggleGroup(optGroup.value)}
          >
            <span class="flex text-left">
              {#if optGroup.icon}
                <span class="mr-s8 h-s24 w-s24 fill-current">
                  {@html optGroup.icon}
                </span>
              {/if}
              {optGroup.label}
            </span>

            <span class="h-s24 w-s24 text-gray-text">
              {#if open}
                {@html arrowUpSIcon}
              {:else}
                {@html arrowDownSIcon}
              {/if}
            </span>
          </button>
          <div class:hidden={!open}>
            <SelectOptions
              {value}
              extraClass="pl-s24 py-s12 pr-s8"
              {isMultiple}
              {selectedOption}
              choices={getChoicesFromKey(optGroup.value, choices)}
              {setAsSelected}
              {updateValue}
            />
            <hr class="mt-s12 text-gray-02" />
          </div>
        </div>
      {:else}
        <SelectOptions
          {value}
          {isMultiple}
          {selectedOption}
          {choices}
          {setAsSelected}
          {updateValue}
        />
      {/each}
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
  .filter-search .has-sub-value-selected {
    @apply text-magenta-cta;
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
