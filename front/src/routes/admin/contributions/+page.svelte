<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { getServiceSuggestions } from "$lib/requests/admin";
  import { onMount } from "svelte";
  import List from "./list.svelte";

  interface Props {
    suggestions: unknown;
  }

  let { suggestions = $bindable() }: Props = $props();

  async function handleRefresh() {
    suggestions = null;
    suggestions = await getServiceSuggestions();
  }

  onMount(async () => {
    suggestions = await getServiceSuggestions();
  });
</script>

<CenteredGrid>
  <h2>Contributions</h2>

  {#if suggestions}
    <List {suggestions} onRefresh={handleRefresh} />
  {:else}
    Chargement…
  {/if}
</CenteredGrid>
