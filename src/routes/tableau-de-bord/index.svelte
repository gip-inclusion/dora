<script context="module">
  import { getMyServices } from "$lib/services";
  import { getMyStructures } from "$lib/structures";

  export async function load({ _page, _fetch, _session, _context }) {
    return {
      props: {
        services: await getMyServices(),
        structures: await getMyStructures(),
      },
    };
  }
</script>

<script>
  import { userInfo } from "$lib/auth";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";

  import StructuresList from "./_structures-list.svelte";
  import ServicesList from "./_services-list.svelte";

  export let services;
  export let structures;
</script>

<svelte:head>
  <title>Tableau de bord | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
    <div class="flex flex-row col-span-full justify-between">
      <h2 class="col-start-1 col-span-full">
        Bonjour {$userInfo.shortName},
      </h2>
    </div>
    <div class="col-start-1 col-span-full text-left">
      {#if $userInfo.isStaff}
        <div class="rounded-md p-s8 bg-gray-bg mb-s48">
          <h4 class="text-information">
            ⚠️ Seulement pour les super-utilisateurs
          </h4>
          <div class="flex">
            <LinkButton
              label="Créer une structure"
              to="/tableau-de-bord/structures/creer"
              noBackground
            />

            <LinkButton
              label="Afficher toutes les structures"
              to="/tableau-de-bord/admin/structures"
              noBackground
            />

            <LinkButton
              label="Afficher tous les services"
              to="/tableau-de-bord/admin/services"
              noBackground
            />
          </div>
        </div>
      {/if}

      {#if structures.length}
        <div class="mb-s8">
          <h2>Mes Structures</h2>
        </div>
        <div class="border-t border-gray-03" />
        <StructuresList {structures} />
      {/if}

      {#if services.length}
        <div class="mb-s8">
          <h2>Mes Services</h2>
        </div>
        <div class="border-t border-gray-03" />
        <ServicesList {services} />
      {/if}
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
