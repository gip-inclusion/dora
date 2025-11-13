<script lang="ts">
  import { formatErrors } from "$lib/validation/validation";

  interface Props {
    id: string;
    group: any;
    choices: any;
    disabled?: boolean;
    readonly?: boolean;
    errorMessages?: string[];
    onchange?: (event: Event) => void;
    horizontal?: boolean;
  }

  let {
    id,
    group = $bindable(),
    choices,
    disabled = false,
    readonly = false,
    errorMessages = [],
    onchange,
    horizontal = false,
  }: Props = $props();

  let focusValue = $state(undefined);
</script>

<div class="gap-s8 flex {horizontal ? 'flex-row' : 'flex-col'}">
  {#each choices as choice, i}
    <label
      class="focus-within:shadow-focus p-s2 flex flex-row items-center rounded outline-0"
      class:outline={choice.value === focusValue}
      class:horizontal-divider={horizontal && i > 0}
      class:opacity-50={disabled}
      class:cursor-not-allowed={disabled}
      class:cursor-pointer={!disabled}
    >
      <input
        id={`${id}-${i}`}
        bind:group
        {onchange}
        onfocus={() => (focusValue = choice.value)}
        onblur={() => (focusValue = undefined)}
        value={choice.value}
        name={id}
        type="radio"
        class="sr-only"
        {disabled}
        {readonly}
        aria-describedby={formatErrors(id, errorMessages)}
      />
      <div
        class="toggle-path h-s24 w-s24 border-gray-03 flex shrink-0 justify-center rounded-full border bg-white"
      >
        <div
          class="toggle-circle h-s12 w-s12 bg-magenta-cta hidden self-center rounded-full"
        ></div>
      </div>
      <span class="ml-s16 text-f16 text-gray-text inline-block">
        {choice.label}
      </span>
    </label>
  {/each}
</div>

<style lang="postcss">
  @reference "../../../app.css";

  input[type="radio"]:checked + div div {
    @apply block;
  }

  .horizontal-divider {
    @apply border-gray-03 px-s16 border-l;
  }
</style>
