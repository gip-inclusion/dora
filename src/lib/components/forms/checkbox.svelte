<script>
  export let group, value, label;
</script>

<style lang="postcss">
  input[type="checkbox"]:checked + div div {
    @apply block;
  }
</style>

<label class="flex flex-row items-center">
  <input bind:group {value} class="hidden" type="checkbox" />
  <div
    class="flex justify-center flex-shrink-0 w-3 h-3 border rounded border-gray-03">
    <div class="self-center hidden w-3/2 h-3/2 bg-dora-magenta-cta" />
  </div>
  <span class="inline-block w-40 ml-2 ">{label}</span>
</label>
