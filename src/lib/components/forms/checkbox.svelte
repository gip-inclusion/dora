<script>
  export let group, value, label;
</script>

<style lang="postcss">
  input[type="checkbox"]:checked + div div {
    @apply block;
  }
</style>

<!-- svelte-ignore a11y-label-has-associated-control -->
<label class="flex flex-row items-center">
  {#if group}
    <input bind:group {value} class="hidden" type="checkbox" />
  {:else}
    <input bind:checked={value} class="hidden" type="checkbox" />
  {/if}
  <div
    class="flex justify-center flex-shrink-0 w-3 h-3 border rounded border-gray-03">
    <div class="self-center hidden w-3/2 h-3/2 bg-dora-magenta-cta" />
  </div>
  <span class="inline-block w-40 ml-2 ">{label}</span>
</label>
