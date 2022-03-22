<script context="module">
  export async function load({ stuff }) {
    return {
      props: {
        structure: stuff.structure,
        services: stuff.services,
      },
    };
  }
</script>

<script>
  import { userInfo } from "$lib/auth";

  import ServicesList from "./services/_list.svelte";
  import Informations from "./_informations.svelte";

  export let structure, services;
</script>

<svelte:head>
  <title>{structure.name} | DORA</title>
  <meta name="description" content={structure.shortDesc} />
</svelte:head>

<Informations {structure} />

{#if !!services.length || structure.isMember || $userInfo.isStaff}
  <div class="col-span-full mb-s24 border-b border-b-gray-03" />
  <ServicesList {structure} services={services.slice(0, 3)} hasButton />
{/if}
