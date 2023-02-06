<script lang="ts">
  export let items = [];
  export let itemId = undefined;
</script>

<ul class="flex gap-s8 overflow-x-auto pt-s16 font-bold">
  {#each items as item}
    <li>
      {#if itemId === item.id}
        <span
          class="block flex items-center rounded-t-md bg-white p-s16 text-france-blue"
        >
          <span class="mr-s8 h-s24 w-s24 fill-current">
            {@html item.icon}
          </span>
          {item.name}
        </span>
      {:else}
        <a
          href={item.href}
          class="block flex items-center rounded-t-md bg-magenta-dark p-s16 text-white"
        >
          <span class="mr-s8 h-s24 w-s24 fill-current">
            {@html item.icon}
          </span>
          {item.name}
        </a>
      {/if}
    </li>
  {/each}
</ul>
