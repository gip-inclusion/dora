<script lang="ts">
  import { getSavedSearchQueryString } from "$lib/requests/saved-search";
  import type { SavedSearch } from "$lib/types";

  export let search: SavedSearch;
  const onSiteOnly = search.locationKinds.toString() === "en-presentiel";
  const remoteOnly = search.locationKinds.toString() === "a-distance";
</script>

<h2 class="text-f20">
  <a href={`/recherche?${getSavedSearchQueryString(search)}`}>
    Services d’insertion
    {#if onSiteOnly}
      en présentiel
    {:else if remoteOnly}
      à distance
    {/if}
    à proximité de {search.cityLabel}

    {#if search.category}
      pour la thématique {search.categoryDisplay}
    {/if}
  </a>
</h2>
