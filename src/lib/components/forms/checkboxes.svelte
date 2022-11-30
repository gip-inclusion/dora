<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let group, choices, disabled, name, readonly;

  const dispatch = createEventDispatcher();

  // We want the change event to come from this component, not from
  // the individual checkboxes, in order to be able to validate properly
  function handleChange() {
    dispatch("change", name);
  }
</script>

<div class="flex flex-col gap-s8">
  {#each choices as choice}
    <label class="flex flex-row items-center">
      <input
        bind:group
        on:change={handleChange}
        value={choice.value}
        type="checkbox"
        class="hidden"
        {disabled}
        {readonly}
      />
      <div
        class="flex h-s24 w-s24 shrink-0 justify-center rounded border border-gray-03"
      >
        <div class="hidden h-s12 w-s12 self-center bg-magenta-cta" />
      </div>
      <span class="ml-s16 inline-block text-f14 text-gray-text"
        >{choice.label}</span
      >
    </label>
  {/each}
</div>

<style lang="postcss">
  input[type="checkbox"]:checked + div div {
    @apply block;
  }
</style>
