<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let id: string,
    group,
    choices,
    disabled = false,
    name: string,
    readonly = false;

  const dispatch = createEventDispatcher();

  // We want the change event to come from this component, not from
  // the individual radio buttons, in order to be able to validate properly
  function handleChange() {
    dispatch("change", name);
  }
</script>

<div class="flex flex-col gap-s8">
  {#each choices as choice, i}
    <label class="flex flex-row items-center focus-within:shadow-focus">
      <input
        id={`${id}-${i}`}
        bind:group
        on:change={handleChange}
        value={choice.value}
        type="radio"
        class="hidden"
        {disabled}
        {readonly}
      />
      <div
        class="toggle-path flex h-s24 w-s24 shrink-0 justify-center rounded-full border border-gray-03 bg-white "
      >
        <div
          class="toggle-circle hidden h-s12 w-s12 self-center rounded-full bg-magenta-cta"
        />
      </div>
      <span class="ml-s16 inline-block text-f14 text-gray-text">
        {choice.label}
      </span>
    </label>
  {/each}
</div>

<style lang="postcss">
  input[type="radio"]:checked + div div {
    @apply block;
  }
</style>
