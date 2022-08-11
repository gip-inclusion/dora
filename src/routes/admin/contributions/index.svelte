<script>
  import { onMount } from "svelte";
  import { getServiceSuggestions } from "$lib/services";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import List from "./_list.svelte";

  export let suggestions;

  async function handleRefresh() {
    suggestions = null;
    suggestions = await getServiceSuggestions();
  }

  onMount(async () => {
    suggestions = await getServiceSuggestions();
  });
</script>

<svelte:head>
  <title>Admin | Contributions | DORA</title>
</svelte:head>

<CenteredGrid bgColor="bg-gray-bg">
  <h2>Contributions</h2>

  {#if suggestions}
    <List {suggestions} onRefresh={handleRefresh} />
  {:else}
    Chargement…
  {/if}
</CenteredGrid>
