<script>
  export let onSelectedChange;
  export let items = [];
  export let itemId = undefined;
</script>

<ul class="flex flex-wrap gap-s8 pt-s16">
  {#each items as item}
    <li>
      <button
        class="rounded-t-md p-s16 {itemId === item.id
          ? 'bg-white text-france-blue '
          : 'bg-magenta-dark text-white '}"
        on:click={() => {
          onSelectedChange(item.id);
        }}>{item.name}</button
      >
    </li>
  {/each}
</ul>
