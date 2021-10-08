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
  import ServicesList from "$lib/components/services-list.svelte";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import StructuresList from "$lib/components/structures-list.svelte";
  import { settingsIcon } from "$lib/icons";

  export let services;
  export let structures;
</script>

<EnsureLoggedIn>
  <CenteredGrid --col-bg="var(--col-gray-00)">
    <div class="flex flex-row col-span-full justify-between">
      <h2 class="col-start-1 col-span-full">
        Bonjour{#if $userInfo.name}&nbsp;{$userInfo.name}{/if},
      </h2>
      <LinkButton
        label="Ma structure"
        noBackground
        icon={settingsIcon}
        iconOnRight
        to={`/tableau-de-bord/structures/${structures[0].slug}`} />
    </div>
    <div class="col-start-1 col-span-full text-left">
      {#if $userInfo.isStaff}
        <div class="flex">
          <LinkButton
            label="Créer une structure"
            to="/structures/creer"
            noBackground />

          <LinkButton
            label="Référencer un service"
            to="/services/creer"
            noBackground />
        </div>
      {/if}

      <div class="mb-4">
        <h2>Services</h2>
      </div>
      <div class="border-t border-gray-03" />

      <ServicesList {services} />

      <div class="mb-4">
        <h2>Structures</h2>
      </div>
      <div class="border-t border-gray-03" />
      <StructuresList {structures} />
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
