<script lang="ts">
  import type { ServiceSearchResult } from "$lib/types";

  import type { PageData } from "./$types";
  import SearchResultCard from "./search-result-card.svelte";

  interface Props {
    data: PageData;
    services: ServiceSearchResult[];
    selectedServiceSlug?: string;
    summarized?: boolean;
  }

  let {
    data,
    services,
    selectedServiceSlug,
    summarized = false,
  }: Props = $props();
</script>

<div class="gap-s16 flex flex-col">
  <h2 class="sr-only">Résultats de votre recherche</h2>
  <div class="gap-s16 flex flex-col">
    {#each services as service}
      <SearchResultCard
        result={service}
        searchId={data.searchId}
        selected={service.slug === selectedServiceSlug}
        {summarized}
      />
    {/each}
  </div>
</div>
