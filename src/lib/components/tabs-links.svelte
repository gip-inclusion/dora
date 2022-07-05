<script>
  export let items = [];
  export let itemId = undefined;
</script>

<ul class="flex flex-wrap gap-s8 pt-s16 font-bold">
  {#each items as item}
    <li>
      {#if itemId === item.id}
        <span class="block rounded-t-md bg-white p-s16 text-france-blue"
          >{item.name}</span
        >
      {:else}
        <a
          href={item.href}
          class="block rounded-t-md bg-magenta-dark p-s16 text-white"
          >{item.name}</a
        >
      {/if}
    </li>
  {/each}
</ul>
