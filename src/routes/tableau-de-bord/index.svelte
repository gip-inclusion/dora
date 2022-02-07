<script context="module">
  import { getMyServices } from "$lib/services";
  import { getMyStructures, getMyPendingStructures } from "$lib/structures";

  export async function load() {
    return {
      props: {
        services: await getMyServices(),
        structures: await getMyStructures(),
        pendingStructures: await getMyPendingStructures(),
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
  import PendingNotice from "./_pending-notice.svelte";

  export let services, structures, pendingStructures;

  async function handleRefresh() {
    services = await getMyServices();
  }
</script>

<svelte:head>
  <title>Tableau de bord | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
    <h2 class="col-span-full">
      Bonjour {$userInfo.shortName},
    </h2>
    <div
      class="col-span-full justify-between rounded-md bg-white p-s16 lg:flex lg:flex-row lg:gap-s16"
    >
      <div class="mb-s16 lg:mb-s0">
        <h4 class="text-magenta-cta">Aidez-nous à améliorer DORA !</h4>
        <p class="text-f14">
          Faites-nous part de vos retours d’expérience, de problèmes que vous
          rencontrez ou de propositions d’amélioration.
        </p>
      </div>
      <div class="shrink-0 self-end py-s16">
        <a
          href="https://itou.typeform.com/to/DPQOe5pP"
          target="_blank"
          rel="noopener nofollow"
          label="Participer (3min)"
          class="rounded bg-magenta-cta px-s16 py-s12 text-f16 font-bold text-white hover:bg-magenta-hover focus:shadow-focus active:bg-france-blue"
          >Participer (3 min.)</a
        >
      </div>
    </div>
    <div class="col-span-full">
      {#if $userInfo.isStaff}
        <div class="mb-s48 rounded-md bg-gray-bg p-s8">
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
      {#if $userInfo.isBizdev}
        <div class="mb-s48 rounded-md bg-gray-bg p-s8">
          <h4 class="text-information">⚠️ Seulement pour les bizdev</h4>
          <div class="flex">
            <LinkButton
              label="Voir les suggestions de service"
              to="/tableau-de-bord/service-suggestions"
              noBackground
            />
          </div>
        </div>
      {/if}
      {#if pendingStructures.length}
        {#each pendingStructures as structure}
          <PendingNotice {structure} />
        {/each}
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
        <ServicesList {services} onRefresh={handleRefresh} />
      {/if}
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
