<script lang="ts">
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { getStructure } from "$lib/requests/structures";
  import { refreshUserInfo } from "$lib/utils/auth";
  import StructureEditionForm from "./structure-edition-form.svelte";
  import { structure } from "../store";
  import type { PageData } from "./$types";
  import type { NationalLabel } from "$lib/types";

  export let data: PageData;

  // StructureOptions contient un champ `restrictedNationalsLabel` permettant
  // de ne pas afficher certains labels qui ne sont pas modifiable par l'utilisateur.
  const filteredNationalLabels = data.structuresOptions.nationalLabels.filter(
    // J'avais rajouté un type pour permettre de filtrer sans avoir à faire ça :(
    // preneur d'une solution plus propre / concise.
    (elt) =>
      !data.structuresOptions.restrictedNationalLabels.find(
        (restricted: NationalLabel) =>
          elt.value === restricted.value && elt.label === restricted.label
      )
  );
  const structuresOptions = {
    ...data.structuresOptions,
    nationalLabels: filteredNationalLabels,
  };

  async function handleRefresh() {
    $structure = await getStructure($structure.slug);

    await refreshUserInfo();
  }
</script>

<EnsureLoggedIn>
  <h2 class="mb-s40 border-b border-gray-02 pb-s40">Informations</h2>

  <StructureEditionForm
    structure={$structure}
    {structuresOptions}
    modify
    onRefresh={handleRefresh}
  />
</EnsureLoggedIn>
