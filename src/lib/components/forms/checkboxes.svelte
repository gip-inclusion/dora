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
        class="flex justify-center shrink-0 w-s24 h-s24 border rounded border-gray-03"
      >
        <div class="self-center hidden w-s12 h-s12 bg-magenta-cta" />
      </div>
      <span class="inline-block ml-s16 text-gray-text text-f14"
        >{choice.label}</span
      >
    </label>
  {/each}
</div>
