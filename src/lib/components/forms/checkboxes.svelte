<script>
  export let group, choices;
</script>

<style lang="postcss">
  input[type="checkbox"]:checked + div div {
    @apply block;
  }
</style>

{#each choices as choice}
  <label class="flex flex-row items-center">
    <input
      on:invalid
      on:blur
      on:input
      bind:group
      value={choice.value}
      type="checkbox"
      class="hidden" />
    <div
      class="flex justify-center flex-shrink-0 w-3 h-3 border rounded border-gray-03">
      <div class="self-center hidden w-3/2 h-3/2 bg-dora-magenta-cta" />
    </div>
    <span class="inline-block w-40 ml-2 ">{choice.displayName}</span>
  </label>
{/each}
