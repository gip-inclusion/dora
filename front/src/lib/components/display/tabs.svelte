<script lang="ts" generics="T extends string">
  interface Props {
    onSelectedChange: (id: T) => void;
    items?: { id: T; name: string }[];
    itemId?: T;
  }

  let { onSelectedChange, items = [], itemId }: Props = $props();
</script>

<ul class="gap-s8 pt-s16 flex overflow-x-auto" role="tablist">
  {#each items as item}
    <li role="presentation">
      <button
        id={`tab-${item.id}`}
        role="tab"
        aria-selected={itemId === item.id}
        class={[
          "px-s20 py-s12 rounded-t font-bold whitespace-nowrap",
          itemId === item.id
            ? "text-france-blue bg-white"
            : "bg-magenta-dark text-white",
        ]}
        onclick={() => {
          onSelectedChange(item.id);
        }}>{item.name}</button
      >
    </li>
  {/each}
</ul>
