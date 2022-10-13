<script lang="ts">
  import FieldWrapper from "../field-wrapper.svelte";
  import { checkIcon, arrowDownSIcon, arrowUpSIcon } from "$lib/icons";

  import { uid } from "uid";
  import { clickOutside } from "$lib/components/use/click-outside";
  import type { Choice } from "$lib/types";
  import SelectLabel from "./select-label.svelte";
  import { getChoiceFromValue } from "$lib/utils/choice";

  export let label: string;
  export let name: string;
  export let minDropdownWidth = "min-w-full";
  export let value: string | string[];
  export let placeholder = "";
  export let helper = "";
  export let required = false;
  export let isMultiple = false;
  export let hideLabel = false;
  export let showIconForSelectedOption = false;
  export let choices: Choice[];
  export let display: "horizontal" | "vertical" = "horizontal";
  export let style: "common" | "filter" = "common";
  export let errorMessages: string[] | undefined = undefined;
  export let handleEltChange: (d: { detail: string }) => void | undefined =
    undefined;

  let ariaDescribedBy = "";

  // AriaDescribedBy => TODO: move to wrapper
  $: {
    ariaDescribedBy = helper ? `${name}-helper` : "";
    if ((errorMessages || []).length) {
      ariaDescribedBy = `${ariaDescribedBy} ${name}-error`;
    }
  }

  // *** Accessibilité
  const uuid: string = uid(); // Pour éviter les conflits d'id si le composant est présent plusieurs fois sur la page
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
          updateValue(selectedOption.value);
        }
      }
    }

    if (event.code === "ArrowDown") {
      selectedOptionIndex = (selectedOptionIndex || 0) + 1;
      selectedOptionIndex = selectedOptionIndex % choices.length;

      selectedOption = choices[selectedOptionIndex];

      scrollToOption(selectedOption.value);
    }
    if (event.code === "ArrowUp") {
      selectedOptionIndex = (selectedOptionIndex || 0) - 1;
      if (selectedOptionIndex < 0) selectedOptionIndex = choices.length - 1;
      selectedOption = choices[selectedOptionIndex];

      scrollToOption(selectedOption.value);
    }
  }

  function scrollToOption(id: string) {
    const scrollTop = document.getElementById(id).offsetTop;
    document.getElementById(`listbox-values-${uuid}`).scrollTop = scrollTop - 5;
  }

  function updateValue(newValue: string) {
    // As array
    if (isMultiple) {
      if (value.includes(newValue)) {
        value = (value as string[]).filter((v) => v !== newValue);
      } else {
        value = [...value, newValue];
      }
    } else {
      // As string
      value = newValue;
    }
    if (handleEltChange) handleEltChange({ detail: name });
    if (!isMultiple) toggleCombobox(false);
  }

  function toggleCombobox(forceValue?: boolean) {
    expanded = forceValue !== undefined ? forceValue : !expanded;
    if (expanded) {
      selectedOptionIndex = 0;
      selectedOption = choices[selectedOptionIndex];
    } else {
      selectedOptionIndex = null;
      selectedOption = null;
    }
  }

  function setAsSelected(index: number) {
    selectedOptionIndex = index;
    selectedOption = choices[selectedOptionIndex];
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
    class="combobox relative w-full rounded border border-gray-03 bg-white p-s12 font-sans disabled:bg-gray-bg disabled:text-gray-text-alt {display}"
    class:filter-style={style === "filter"}
    class:expanded
    class:has-value={value}
    role="combobox"
    tabindex="0"
    aria-describedby={ariaDescribedBy}
    on:click={() => toggleCombobox()}
    on:keydown={handleKeydown}
    use:clickOutside
    on:click_outside={() => toggleCombobox(false)}
  >
    <div class="current-value flex cursor-pointer items-center justify-between">
      <div class="overflow-hidden text-ellipsis whitespace-nowrap">
        {#if isMultiple && value.length > 0}
          {value
            .map((v) => choices.find((c) => c.value === v).label)
            .join(", ")}
        {:else if !isMultiple && value}
          <SelectLabel
            choice={getChoiceFromValue(value, choices)}
            useSelectedLabel
            showIcon={showIconForSelectedOption}
          />
        {:else}
          <span class="placeholder text-gray-text-alt">{placeholder}</span>
        {/if}
      </div>

      <div class="h-s24 w-s24">
        <span class="chevron h-s24 w-s24 fill-current text-magenta-cta">
          {#if expanded}
            {@html arrowUpSIcon}
          {:else}
            {@html arrowDownSIcon}
          {/if}
        </span>
      </div>
    </div>

    <div
      class:hidden={!expanded}
      class="absolute top-[52px] left-s0 z-20 flex max-h-s512 flex-col gap-s10 rounded border border-gray-00 bg-white p-s12 shadow-md {minDropdownWidth}"
      role="listbox"
      id={`listbox-values-${uuid}`}
      aria-labelledby={`button-label-${uuid}`}
      tabindex="-1"
    >
      {#each choices as option, index (option.value)}
        {@const selected = isMultiple
          ? value.includes(option.value)
          : option.value === value}
        <div
          class="flex min-h-[36px] w-full cursor-pointer items-center justify-between p-s6 text-gray-dark"
          role="option"
          id={option.value}
          class:hover={option.value === selectedOption?.value}
          class:selected
          on:click|stopPropagation={() => updateValue(option.value)}
          on:mouseenter={() => setAsSelected(index)}
        >
          <SelectLabel choice={getChoiceFromValue(option.value, choices)} />

          <span class="h-s24 w-s24 fill-current">
            {#if selected}
              {@html checkIcon}
            {/if}
          </span>
        </div>
      {/each}
    </div>
  </div>
</FieldWrapper>

<style lang="postcss">
  .selected {
    @apply text-magenta-cta;
  }

  @screen lg {
    .vertical {
      @apply lg:w-3/4;
    }
  }

  .hover {
    @apply bg-gray-bg;
  }

  /* As filter */
  .filter-style {
    @apply rounded-xl px-s16 py-s12;
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
