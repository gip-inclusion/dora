<script>
  export let group, choices, disabled, name;
</script>

<style lang="postcss">
  input[type="checkbox"]:checked + div div {
    @apply block;
  }
</style>

{#each choices as choice}
  <label class="flex flex-row items-center">
    <input
      on:blur
      bind:group
      {name}
      value={choice.value}
      type="checkbox"
      class="hidden"
      {disabled} />
    <div
      class="flex justify-center flex-shrink-0 w-3 h-3 border rounded border-gray-03">
      <div class="self-center hidden w-3/2 h-3/2 bg-dora-magenta-cta" />
    </div>
    <span class="inline-block w-40 ml-2 text-gray-text text-sm"
      >{choice.displayName}</span>
  </label>
{/each}
