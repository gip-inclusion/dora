<script lang="ts">
  import type { AdminStructure } from "$lib/types";

  import StructureCard from "./structure-card.svelte";

  interface Props {
    filteredStructures: AdminStructure[];
    selectedStructureSlug: string | null;
    onRefresh: () => void | Promise<void>;
  }

  let {
    filteredStructures,
    selectedStructureSlug = $bindable(),
    onRefresh,
  }: Props = $props();
</script>

<div class="gap-s16 flex flex-col">
  {#each filteredStructures as structure (structure.slug)}
    <StructureCard
      {structure}
      highlighted={selectedStructureSlug === structure.slug}
      onHover={(slug) => (selectedStructureSlug = slug)}
      {onRefresh}
    />
  {/each}
</div>
