<script lang="ts">
  export let onSelectedChange;
  export let items: { id: string; name: string }[] = [];
  export let itemId: string | undefined = undefined;
</script>

<ul class="gap-s8 pt-s16 flex flex-wrap">
  {#each items as item}
    <li>
      <button
        class="px-s20 py-s12 rounded-t font-bold {itemId === item.id
          ? 'text-france-blue bg-white'
          : 'bg-magenta-dark text-white'}"
        on:click={() => {
          onSelectedChange(item.id);
        }}>{item.name}</button
      >
    </li>
  {/each}
</ul>
