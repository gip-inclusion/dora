<script lang="ts">
  import { checkIcon } from "$lib/icons";
  import type { Choice } from "$lib/types";
  import CheckboxMark from "$lib/components/display/checkbox-mark.svelte";
  import { getChoiceFromValue } from "$lib/utils/choice";
  import SelectLabel from "./select-label.svelte";

  export let value: string | string[];
  export let isMultiple: boolean;
  export let selectedOption: Choice | undefined;
  export let choices: Choice[];
  export let extraClass = "";

  export let setAsSelected: (i: string | null) => void;
  export let updateValue: (i: string) => void;
</script>

{#each choices as option (option.value)}
  {@const selected = isMultiple
    ? value.includes(option.value)
    : option.value === value}

  <div
    class="option flex min-h-[36px] w-full cursor-pointer p-s6 text-gray-dark {isMultiple
      ? 'items-start gap-s8'
      : 'items-center justify-between'} {extraClass}"
    role="option"
    aria-selected={selected}
    id={option.value}
    class:hover={option.value === selectedOption?.value}
    class:selected
    tabindex="0"
    on:keypress={(event) => {
      if (event.code === "Enter") {
        updateValue(option.value);
      }
    }}
    on:click|stopPropagation={() => updateValue(option.value)}
    on:mouseenter={() => setAsSelected(option.value)}
    on:mouseleave={() => setAsSelected(null)}
  >
    {#if isMultiple}
      <CheckboxMark checked={selected} />
    {/if}

    <SelectLabel choice={getChoiceFromValue(option.value, choices)} />

    {#if !isMultiple}
      <span class="h-s24 w-s24 fill-current text-magenta-cta" class:selected>
        {#if selected}
          {@html checkIcon}
        {/if}
      </span>
    {/if}
  </div>
{/each}

<style lang="postcss">
  .hover {
    @apply bg-magenta-10 text-magenta-cta;
  }
</style>
