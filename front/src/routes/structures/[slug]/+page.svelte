<script lang="ts">
  import { getStructure } from "$lib/requests/structures";
  import type { PageData } from "./$types";
  import BranchesList from "./antennes/list.svelte";
  import Informations from "./informations.svelte";
  import ModelesList from "./modeles/list.svelte";
  import ServicesList from "./services/list.svelte";
  import { structure } from "./store";

  export let data: PageData;

  async function handleRefresh() {
    $structure = await getStructure($structure.slug);
  }
</script>

<Informations
  structure={$structure}
  members={data.members}
  putativeMembers={data.putativeMembers}
  structuresOptions={data.structuresOptions}
/>
<div class="mb-s64" />

{#if !!$structure.services?.length}
  <hr class="mb-s24" />
  <ServicesList
    structure={$structure}
    tabDisplay={false}
    onRefresh={handleRefresh}
    total={$structure.services.length}
    limit={3}
  />
{/if}

{#if !!$structure.models?.length && $structure.canEditServices}
  <hr class="mb-s24" />
  <ModelesList
    structure={$structure}
    models={$structure.models}
    tabDisplay={false}
    total={$structure.models.length}
    limit={4}
  />
{/if}

{#if !$structure.parent && $structure.branches?.length}
  <hr class="mb-s24" />
  <BranchesList
    structure={$structure}
    branches={$structure.branches || []}
    tabDisplay={false}
    total={$structure.branches.length}
    limit={4}
  />
{/if}
