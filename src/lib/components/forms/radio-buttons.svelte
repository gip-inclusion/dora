<script>
  export let group, choices, disabled;
</script>

<style lang="postcss">
  input[type="radio"]:checked + div div {
    @apply block;
  }
</style>

{#each choices as choice}
  <label class="flex flex-row items-center focus-within:shadow-focus">
    <input
      type="radio"
      on:blur
      on:input
      bind:group
      value={choice.value}
      class="hidden"
      {disabled} />
    <div
      class="flex justify-center w-3 h-3 bg-white border rounded-full toggle-path border-gray-03 ">
      <div
        class="self-center hidden rounded-full w-3/2 h-3/2 bg-dora-magenta-cta toggle-circle" />
    </div>
    <span class="inline-block w-40 ml-2 text-gray-text text-sm"
      >{choice.displayName}</span>
  </label>
{/each}
