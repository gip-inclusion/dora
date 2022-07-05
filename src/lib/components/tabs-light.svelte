<script>
  export let onSelectedChange;
  export let items = [];
  export let itemId = undefined;
</script>

<ul class="flex flex-wrap gap-s8">
  {#each items as item}
    <li>
      <button
        class="px-s10 py-s6 text-f14 font-bold text-gray-text hover:text-magenta-cta "
        class:active={itemId === item.id}
        on:click={() => {
          onSelectedChange(item.id);
        }}>{item.name}</button
      >
    </li>
  {/each}
</ul>

<style lang="postcss">
  .active {
    @apply rounded border border-magenta-cta text-magenta-cta;
  }
</style>
