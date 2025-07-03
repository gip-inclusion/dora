<script lang="ts">
  import { stopPropagation } from 'svelte/legacy';

  import { checkIcon } from "$lib/icons";
  import type { Choice } from "$lib/types";
  import CheckboxMark from "$lib/components/display/checkbox-mark.svelte";
  import { getChoiceFromValue } from "$lib/utils/choice";
  import SelectLabel from "./select-label.svelte";


  interface Props {
    value: string | string[];
    isMultiple: boolean;
    selectedOption: Choice | undefined;
    choices: Choice[];
    extraClass?: string;
    setAsSelected: (i: string | null) => void;
    updateValue: (i: string) => void;
  }

  let {
    value,
    isMultiple,
    selectedOption,
    choices,
    extraClass = "",
    setAsSelected,
    updateValue
  }: Props = $props();
</script>

{#each choices as option (option.value)}
  {@const selected = isMultiple
    ? value.includes(option.value)
    : option.value === value}

  <div
    class="option p-s6 text-gray-dark flex min-h-[36px] w-full cursor-pointer {isMultiple
      ? 'gap-s8 items-start'
      : 'items-center justify-between'} {extraClass}"
    role="option"
    aria-selected={selected}
    id={option.value}
    class:hover={option.value === selectedOption?.value}
    class:selected
    tabindex="0"
    onkeypress={(event) => {
      if (event.code === "Enter") {
        updateValue(option.value);
      }
    }}
    onclick={stopPropagation(() => updateValue(option.value))}
    onmouseenter={() => setAsSelected(option.value)}
    onmouseleave={() => setAsSelected(null)}
  >
    {#if isMultiple}
      <CheckboxMark checked={selected} />
    {/if}

    <SelectLabel choice={getChoiceFromValue(option.value, choices)} />

    {#if !isMultiple}
      <span class="h-s24 w-s24 text-magenta-cta fill-current" class:selected>
        {#if selected}
          {@html checkIcon}
        {/if}
      </span>
    {/if}
  </div>
{/each}

<style lang="postcss">
  @reference "../../../../app.css";

  .hover {
    @apply bg-magenta-10 text-magenta-cta;
  }
</style>
