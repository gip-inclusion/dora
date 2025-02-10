<script lang="ts">
  import type { TabItem } from "./header.svelte";

  export let items: TabItem[] = [];
  export let itemId: string;
</script>

<ul class="gap-s8 pt-s16 flex overflow-x-auto font-bold">
  {#each items as item}
    <li>
      {#if itemId === item.id}
        <span
          class="px-s24 py-s12 text-france-blue flex items-center rounded-t bg-white"
        >
          <span class="mr-s8 h-s24 w-s24 fill-current">
            {@html item.icon}
          </span>
          {item.name}
        </span>
      {:else}
        <a
          href={item.href}
          class="bg-magenta-dark px-s24 py-s12 flex items-center rounded-t text-white"
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
