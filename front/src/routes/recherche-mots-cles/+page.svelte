<script lang="ts">
  import CenteredGrid from "#lib/components/display/centered-grid.svelte";
  import SearchFormByKeyword from "#lib/components/specialized/service-search-keyword.svelte";

  import type { PageData } from "./$types";
  import KeywordSearch from "./keyword-search.svelte";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
</script>

{#if data.hasCriteria}
  <KeywordSearch {data} />
{:else}
  <CenteredGrid extraClass="mb-s32" bgColor="bg-magenta-10">
    <h1 class="mb-s32 text-france-blue m-auto text-center text-balance">
      Trouvez le service adapté<br />pour lever les freins à l’insertion
    </h1>

    <div class="mb-s16">
      <SearchFormByKeyword />
    </div>
  </CenteredGrid>
{/if}
