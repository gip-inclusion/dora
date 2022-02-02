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
    <div class="col-start-1 col-span-full text-left">
      <div class="mb-s8">
        <h2>Suggestions de services</h2>
      </div>
      <div class="border-t border-gray-03" />
      <div class="rounded-md p-s16 mt-s32 bg-gray-bg mb-s48">
        <div class="flex">
          <SuggestionsList {suggestions} onRefresh={handleRefresh} />
        </div>
      </div>
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
