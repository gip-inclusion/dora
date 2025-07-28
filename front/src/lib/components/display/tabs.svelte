<script lang="ts">
  interface Props {
    onSelectedChange: any;
    items?: { id: string; name: string }[];
    itemId?: string;
  }

  let { onSelectedChange, items = [], itemId }: Props = $props();
</script>

<ul class="gap-s8 pt-s16 flex flex-wrap">
  {#each items as item}
    <li>
      <button
        class="px-s20 py-s12 rounded-t font-bold {itemId === item.id
          ? 'text-france-blue bg-white'
          : 'bg-magenta-dark text-white'}"
        onclick={() => {
          onSelectedChange(item.id);
        }}>{item.name}</button
      >
    </li>
  {/each}
</ul>
