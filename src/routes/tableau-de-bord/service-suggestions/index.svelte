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

  import SuggestionsList from "./_suggestions-list.svelte";

  export let suggestions;

  async function handleRefresh() {
    suggestions = await getServiceSuggestions();
  }
</script>

<svelte:head>
  <title>Suggestions de services | DORA</title>
</svelte:head>
<EnsureLoggedIn>
  <CenteredGrid topPadded>
    <div class="col-span-full col-start-1 text-left">
      <div class="mb-s8">
        <h2>Suggestions de services</h2>
      </div>
      <div class="border-t border-gray-03" />
      <div class="mt-s32 mb-s48 rounded-md bg-gray-bg p-s16">
        <div class="flex">
          <SuggestionsList {suggestions} onRefresh={handleRefresh} />
        </div>
      </div>
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
