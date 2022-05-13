<script>
  import { userInfo } from "$lib/auth";
  import { structure } from "./_store.js";
  import { getStructure } from "$lib/structures";

  import Informations from "./_informations.svelte";
  import ServicesList from "./services/_list.svelte";
  import BranchesList from "./antennes/_list.svelte";
  import { capitalize } from "$lib/utils.js";

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

<Informations structure={$structure} />

{#if !!$structure.services?.length || $structure.isMember || $userInfo?.isStaff}
  <hr class="col-span-full mb-s24 border-t border-t-gray-03" />
  <ServicesList
    structure={$structure}
    services={$structure.services}
    hasOptions={false}
    onRefresh={handleRefresh}
    total={$structure.services.length}
    limit={4}
  />
{/if}

{#if !$structure.parent && ($structure.branches?.length || $structure.isAdmin || $userInfo?.isStaff)}
  <hr class="col-span-full mb-s24 border-t border-t-gray-03" />
  <BranchesList
    structure={$structure}
    branches={$structure.branches || []}
    hasOptions={false}
    total={$structure.branches.length}
    limit={4}
  />
{/if}
