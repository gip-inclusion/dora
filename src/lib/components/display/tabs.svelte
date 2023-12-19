<script lang="ts">
  export let onSelectedChange;
  export let items: { id: string; name: string }[] = [];
  export let itemId: string | undefined = undefined;
</script>

<ul class="flex flex-wrap gap-s8 pt-s16">
  {#each items as item}
    <li>
      <button
        class="rounded-t px-s20 py-s12 font-bold {itemId === item.id
          ? 'bg-white text-france-blue'
          : 'bg-magenta-dark text-white'}"
        on:click={() => {
          onSelectedChange(item.id);
        }}>{item.name}</button
      >
    </li>
  {/each}
</ul>
