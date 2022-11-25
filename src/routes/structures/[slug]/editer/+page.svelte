<script lang="ts">
  import { refreshUserInfo } from "$lib/auth";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import StructureFormWrapper from "$lib/components/structures/form-wrapper.svelte";
  import { getStructure } from "$lib/structures";
  import { capitalize } from "$lib/utils";
  import { structure } from "../_store";
  import type { PageData } from "./$types";

  export let data: PageData;

  async function handleRefresh() {
    $structure = await getStructure($structure.slug);

    await refreshUserInfo();
  }
</script>

<svelte:head>
  <title>
    {capitalize($structure.name)} | Éditer | DORA
  </title>
</svelte:head>

<EnsureLoggedIn>
  <h2 class="mb-s40 border-b border-gray-02 pb-s40">Informations</h2>

  <StructureFormWrapper
    structure={$structure}
    structuresOptions={data.structuresOptions}
    modify
    onRefresh={handleRefresh}
  />
</EnsureLoggedIn>
