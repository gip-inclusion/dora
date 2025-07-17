<script lang="ts">
  import { formatErrors } from "$lib/validation/validation";
  import { createEventDispatcher } from "svelte";

  interface Props {
    id: string;
    group: any;
    choices: any;
    disabled?: boolean;
    name: string;
    readonly?: boolean;
    errorMessages?: string[];
  }

  let {
    id,
    group = $bindable(),
    choices,
    disabled = false,
    name,
    readonly = false,
    errorMessages = [],
  }: Props = $props();

  let focusValue = $state(undefined);
  const dispatch = createEventDispatcher();

  // We want the change event to come from this component, not from
  // the individual radio buttons, in order to be able to validate properly
  function handleChange() {
    dispatch("change", name);
  }
</script>

<div class="gap-s8 flex flex-col">
  {#each choices as choice, i}
    <label
      class="focus-within:shadow-focus p-s2 flex flex-row items-center rounded outline-0"
      class:outline={choice.value === focusValue}
    >
      <input
        id={`${id}-${i}`}
        bind:group
        onchange={handleChange}
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
</style>
