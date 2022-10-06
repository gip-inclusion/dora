<script lang="ts">
  import FieldWrapper from "./field-wrapper.svelte";
  import { checkIcon, arrowDownSIcon, arrowUpSIcon } from "$lib/icons";

  import { uid } from "uid";
  import { clickOutside } from "$lib/components/use/click-outside";
  import type { Choice } from "$lib/types";
  import { getLabelFromValue } from "$lib/utils/choice";

  export let label: string;
  export let name: string;
  export let value: string | string[];
  export let placeholder = "";
  export let helper = "";
  export let required = false;
  export let isMultiple = false;
  export let choices: Choice[];
  export let display: "horizontal" | "vertical" = "horizontal";
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

<FieldWrapper {label} {name} {helper} {required} {errorMessages} {display}>
  <div
    id={name}
    aria-controls={`listbox-values-${uuid}`}
    aria-expanded={expanded}
    aria-haspopup="listbox"
    aria-labelledby={`button-label-${uuid}`}
    class="relative w-full rounded border border-gray-03 bg-white p-s12 font-sans disabled:bg-gray-bg disabled:text-gray-text-alt {display}"
    role="combobox"
    tabindex="0"
    aria-describedby={ariaDescribedBy}
    on:click={() => toggleCombobox()}
    on:keydown={handleKeydown}
    use:clickOutside
    on:click_outside={() => toggleCombobox(false)}
  >
    <div class="absolute right-s10 h-s24 w-s24">
      <span class="h-s24 w-s24 fill-current text-magenta-cta">
        {#if expanded}
          {@html arrowUpSIcon}
        {:else}
          {@html arrowDownSIcon}
        {/if}
      </span>
    </div>

    <div class="w-[90%] w-full overflow-hidden text-ellipsis whitespace-nowrap">
      {#if isMultiple && value.length > 0}
        {value.map((v) => choices.find((c) => c.value === v).label).join(", ")}
      {:else if !isMultiple && value}
        {getLabelFromValue(value, choices)}
      {:else}
        <span class="text-gray-text-alt">{placeholder}</span>
      {/if}
    </div>

    <div
      class:hidden={!expanded}
      class="absolute top-[52px] right-s0 z-20 flex max-h-s512 w-full flex-col gap-s10 overflow-y-scroll rounded border border-gray-00 bg-white p-s12 shadow-md"
      role="listbox"
      id={`listbox-values-${uuid}`}
      aria-labelledby={`button-label-${uuid}`}
      tabindex="-1"
    >
      {#each choices as { value: optionValue, label }, index (optionValue)}
        {@const selected = isMultiple
          ? value.includes(optionValue)
          : optionValue === value}
        <div
          class="flex min-h-[36px] cursor-pointer items-center justify-between p-s6 text-gray-text-alt"
          role="option"
          id={optionValue}
          class:hover={optionValue === selectedOption?.value}
          class:selected
          on:click|stopPropagation={() => updateValue(optionValue)}
          on:mouseenter={() => setAsSelected(index)}
        >
          {label}
          {#if selected && optionValue}
            <span class="h-s24 w-s24 fill-current">
              {@html checkIcon}
            </span>
          {/if}
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

  .hover:not(.selected) {
    @apply text-gray-text;
  }
  .hover {
    @apply bg-gray-bg;
  }
</style>
