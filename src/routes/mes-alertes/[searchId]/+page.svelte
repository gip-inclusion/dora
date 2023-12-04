<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";

  import SearchResult from "../../recherche/search-result.svelte";
  import SavedSearchDescription from "../description.svelte";
  import SavedSearchTitle from "../title.svelte";

  export let data;
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1 class="text-center text-france-blue">Mon alerte</h1>

    <div class="mb-s32">
      <Breadcrumb currentLocation="saved-search" dark />
    </div>

    <SavedSearchTitle search={data.savedSearch} />
    <SavedSearchDescription search={data.savedSearch} />

    <div class="mt-s16 mt-s32 text-f21 font-bold text-gray-dark">
      {#if data.recentResults.length > 0}
        {data.recentResults.length}
        {data.recentResults.length > 1
          ? "résultats ajoutés"
          : "résultat ajouté"} à DORA au cours des 30 derniers jours.
      {:else}
        Aucun résultat ajouté à DORA au cours des 30 derniers jours.
      {/if}
    </div>

    {#if data.recentResults.length}
      <div class="mt-s32 flex flex-col gap-s16">
        <h2 class="sr-only">Résultats de votre recherche</h2>
        {#each data.recentResults as result}
          <SearchResult id={`#result-${result.id}`} {result} />
        {/each}
      </div>
    {/if}
  </CenteredGrid>
</EnsureLoggedIn>
