<script lang="ts">
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { getStructure } from "$lib/requests/structures";
  import { refreshUserInfo } from "$lib/utils/auth";
  import StructureEditionForm from "./structure-edition-form.svelte";
  import { structure } from "../store";
  import type { PageData } from "./$types";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  async function handleRefresh() {
    $structure = await getStructure($structure.slug);

    await refreshUserInfo();
  }
</script>

<EnsureLoggedIn>
  <h2 class="mb-s40 border-gray-02 pb-s40 border-b">Informations</h2>

  <StructureEditionForm
    structure={$structure}
    structuresOptions={data.structuresOptions}
    modify
    onRefresh={handleRefresh}
  />
</EnsureLoggedIn>
