<script lang="ts">
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { getStructure } from "$lib/requests/structures";
  import { refreshUserInfo } from "$lib/utils/auth";
  import StructureFormWrapper from "../../form-wrapper.svelte";
  import { structure } from "../store";
  import type { PageData } from "./$types";

  export let data: PageData;

  async function handleRefresh() {
    $structure = await getStructure($structure.slug);

    await refreshUserInfo();
  }
</script>

<EnsureLoggedIn>
  <h2 class="mb-s40 border-b border-gray-02 pb-s40">Informations</h2>

  <StructureFormWrapper
    structure={$structure}
    structuresOptions={data.structuresOptions}
    modify
    onRefresh={handleRefresh}
  />
</EnsureLoggedIn>
