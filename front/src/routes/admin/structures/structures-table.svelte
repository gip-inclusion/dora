<script lang="ts">
  import { URL_MANAGER_DATA_INCLUSION_NOTICE } from "$lib/consts";
  import type { AdminStructure } from "$lib/types";

  import StructureCard from "./structure-card.svelte";

  interface Props {
    filteredStructures: AdminStructure[];
    selectedStructureSlug: string | null;
    onRefresh: () => void;
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

  <aside class="border-info bg-info-light px-s20 py-s16 border-l-4">
    <h3 class="text-f18 text-info mb-s8 leading-28">
      Vous pouvez agir uniquement sur les structures et services créés via Dora
    </h3>
    <p class="text-f14 text-gray-text mb-s0 leading-24">
      Vous voyez dans ce tableau de bord uniquement les services créés dans
      Dora. Les visiteurs voient également les services issus de data·inclusion.
      N’hésitez pas à nous signaler tout problème dans les données
      data·inclusion en suivant
      <a
        href={URL_MANAGER_DATA_INCLUSION_NOTICE}
        target="_blank"
        rel="noopener"
        class="underline">cette notice</a
      >.
    </p>
  </aside>
</div>
