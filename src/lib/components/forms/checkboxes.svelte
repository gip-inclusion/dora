<script>
  import { createEventDispatcher } from "svelte";
  export let group, choices, disabled, name, readonly;

  const dispatch = createEventDispatcher();

  // We want the change event to come from this component, not from
  // the individual checkboxes, in order to be able to validate properly
  function handleChange() {
    dispatch("change", name);
  }
</script>

<style lang="postcss">
  input[type="checkbox"]:checked + div div {
    @apply block;
  }
</style>

<div class="flex flex-col gap-1">
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
        class="flex justify-center flex-shrink-0 w-3 h-3 border rounded border-gray-03"
      >
        <div class="self-center hidden w-3/2 h-3/2 bg-dora-magenta-cta" />
      </div>
      <span class="inline-block w-40 ml-2 text-gray-text text-sm"
        >{choice.label}</span
      >
    </label>
  {/each}
</div>
