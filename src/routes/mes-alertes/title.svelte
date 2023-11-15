<script>
  import { getSavedSearchQueryString } from "$lib/requests/saved-search";
  export let search;
</script>

<h2 class="text-f20">
  <a href={`/recherche?${getSavedSearchQueryString(search)}`}>
    Services d’insertion à proximité de {search.cityLabel}

    {#if search.category}
      pour la thématique {search.categoryDisplay}
    {/if}
  </a>
</h2>
