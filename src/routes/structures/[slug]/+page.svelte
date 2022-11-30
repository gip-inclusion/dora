<script lang="ts">
  import { userInfo } from "$lib/auth";
  import { getStructure } from "$lib/structures";
  import { capitalize } from "$lib/utils";
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

<svelte:head>
  <title>
    {capitalize($structure.name)} | DORA
  </title>
  <meta name="description" content={$structure.shortDesc} />
</svelte:head>

<Informations
  structure={$structure}
  structuresOptions={data.structuresOptions}
/>
<div class="mb-s64" />

{#if !!$structure.services?.length || $structure.isMember || $userInfo?.isStaff}
  <hr class="mb-s24" />
  <ServicesList
    structure={$structure}
    hasOptions={false}
    onRefresh={handleRefresh}
    total={$structure.services.length}
    limit={3}
  />
{/if}

{#if $structure.isMember || $userInfo?.isStaff}
  <hr class="mb-s24" />
  <ModelesList
    structure={$structure}
    models={$structure.models}
    hasOptions={false}
    total={$structure.models.length}
    limit={4}
  />
{/if}

{#if !$structure.parent && $structure.branches?.length}
  <hr class="mb-s24" />
  <BranchesList
    structure={$structure}
    branches={$structure.branches || []}
    hasOptions={false}
    total={$structure.branches.length}
    limit={4}
  />
{/if}
