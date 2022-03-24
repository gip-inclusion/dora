<script context="module">
  export async function load({ stuff }) {
    return {
      props: {
        structure: stuff.structure,
      },
    };
  }
</script>

<script>
  import { userInfo } from "$lib/auth";

  import Informations from "./_informations.svelte";
  import ServicesList from "./services/_list.svelte";
  import AntennesList from "./antennes/_list.svelte";
  import { getStructure } from "$lib/structures";

  export let structure;

  async function handleRefresh() {
    structure = await getStructure(structure.slug);
  }
</script>

<svelte:head>
  <title>{structure.name} | DORA</title>
  <meta name="description" content={structure.shortDesc} />
</svelte:head>

<Informations {structure} />

{#if !!structure.services.length || structure.isMember || $userInfo?.isStaff}
  <div class="col-span-full mb-s24 border-b border-b-gray-03" />
  <ServicesList
    {structure}
    services={structure.services.slice(0, 3)}
    hasListLink
    onRefresh={handleRefresh}
  />
{/if}

{#if !!structure.branches?.length || structure.isAdmin || $userInfo?.isStaff}
  <div class="col-span-full mb-s24 border-b border-b-gray-03" />
  <AntennesList
    {structure}
    branches={structure.branches?.slice(0, 3) || []}
    hasListLink
  />
{/if}
