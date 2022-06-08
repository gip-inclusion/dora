<script context="module">
  import { getServiceSuggestions } from "$lib/services";

  export async function load() {
    return {
      props: {
        suggestions: await getServiceSuggestions(),
      },
    };
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";

  import List from "./_list.svelte";

  export let suggestions;

  async function handleRefresh() {
    suggestions = await getServiceSuggestions();
  }
</script>

<svelte:head>
  <title>Suggestions de services | DORA</title>
</svelte:head>
<EnsureLoggedIn>
  <CenteredGrid>
    <div class="text-left">
      <h2>Suggestions de services</h2>

      <hr />
      <div class="mt-s32 mb-s48 rounded-md bg-gray-bg p-s16">
        <div class="flex">
          <List {suggestions} onRefresh={handleRefresh} />
        </div>
      </div>
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
