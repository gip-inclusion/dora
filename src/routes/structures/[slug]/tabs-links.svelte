<script lang="ts">
  import type { TabItem } from "./header.svelte";

  export let items: TabItem[] = [];
  export let itemId: string;
</script>

<ul class="flex gap-s8 overflow-x-auto pt-s16 font-bold">
  {#each items as item}
    <li>
      {#if itemId === item.id}
        <span
          class="flex items-center rounded-t bg-white px-s24 py-s12 text-france-blue"
        >
          <span class="mr-s8 h-s24 w-s24 fill-current">
            {@html item.icon}
          </span>
          {item.name}
        </span>
      {:else}
        <a
          href={item.href}
          class="flex items-center rounded-t bg-magenta-dark px-s24 py-s12 text-white"
          data-sveltekit-noscroll
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
