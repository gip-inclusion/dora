<script lang="ts">
  import illuAccompagner from "$lib/assets/illustrations/illu-accompagner.svg";
  import illuMobiliser from "$lib/assets/illustrations/illu-mobiliser.svg";
  import illuRecenser from "$lib/assets/illustrations/illu-recenser.svg";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import DepartmentSelector from "$lib/components/specialized/department-selector.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";

  import {
    AUTOMETA_MANAGER_DASHBOARD_URLS,
    URL_MANAGER_HELP_NOTICE,
  } from "$lib/consts";
  import { getStructuresAdmin } from "$lib/requests/admin";
  import type { AdminStructure, GeoApiValue } from "$lib/types";

  import { getStructureStatus } from "../structures/structures-filters";
  import type { PageData } from "./$types";
  import TerritoryCard from "./territory-card.svelte";
  import TerritoryLink from "./territory-link.svelte";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  let selectedDepartment: GeoApiValue = $state(data.department);
  // `null` tant que les structures du territoire n'ont pas pu être chargées :
  // les compteurs sont remplacés par des spinners plutôt qu'affichés à zéro.
  let structures: AdminStructure[] | null = $state(null);
  let loading = $state(true);

  // Identifie la dernière requête afin d'éviter d'afficher les résultats
  // d'une requête plus ancienne.
  let currentRequestId = 0;

  const autometaUrls = $derived(
    AUTOMETA_MANAGER_DASHBOARD_URLS(selectedDepartment.code)
  );

  const counters = $derived.by(() => {
    const loaded = structures;

    if (!loaded) {
      return null;
    }

    // Mêmes calculs que les filtres du tableau de bord (/admin/structures)
    // afin que les compteurs concordent entre les deux pages.
    return {
      withoutPublishedService: loaded.filter(
        (structure) => getStructureStatus(structure) === "awaitingActivation"
      ).length,
      awaitingModeration: loaded.filter(
        (structure) => getStructureStatus(structure) === "awaitingModeration"
      ).length,
      withOutdatedServices: loaded.filter(
        (structure) => getStructureStatus(structure) === "awaitingUpdate"
      ).length,
    };
  });

  async function loadDepartment(department: GeoApiValue) {
    const requestId = ++currentRequestId;

    selectedDepartment = department;
    structures = null;
    loading = true;

    try {
      const results = await getStructuresAdmin(department.code);

      if (requestId !== currentRequestId) {
        return;
      }

      structures = results ?? null;
    } finally {
      if (requestId === currentRequestId) {
        loading = false;
      }
    }
  }

  loadDepartment(data.department);
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <div class="mb-s32">
      <Breadcrumb currentLocation="manager-homepage" />
    </div>

    <div class="gap-s16 mb-s48 flex flex-col justify-between md:flex-row">
      <div>
        <h1 class="mb-s8 text-france-blue">Gérer mon territoire</h1>

        <div class="text-france-blue">
          {#if data.departments.length > 1}
            <DepartmentSelector
              departments={data.departments}
              {selectedDepartment}
              onChange={loadDepartment}
            />
          {:else}
            <span class="text-f23 font-bold">
              {selectedDepartment.name} ({selectedDepartment.code})
            </span>
          {/if}
        </div>
      </div>

      <div class="shrink-0">
        <LinkButton
          label="Notice"
          to={URL_MANAGER_HELP_NOTICE}
          otherTab
          nofollow
          secondary
        />
      </div>
    </div>

    <div class="gap-s32 grid grid-cols-1 md:grid-cols-3">
      <TerritoryCard
        title="Modifier les structures existantes"
        illustration={illuAccompagner}
        to="/admin/structures"
        ctaLabel="Rechercher une structure à modifier"
      >
        {#snippet links()}
          <TerritoryLink
            label="Structures sans service"
            to="/admin/structures?statut=awaitingActivation"
            count={counters?.withoutPublishedService}
            {loading}
          />
          <TerritoryLink
            label="Administrateurs à valider"
            to="/admin/structures?statut=awaitingModeration"
            count={counters?.awaitingModeration}
            {loading}
          />
          <TerritoryLink
            label="Services à actualiser"
            to="/admin/structures?statut=awaitingUpdate"
            count={counters?.withOutdatedServices}
            {loading}
          />
        {/snippet}
      </TerritoryCard>

      <TerritoryCard
        title="Créer de nouvelles structures"
        illustration={illuRecenser}
        to="/admin/structures/creer"
        ctaLabel="Ajouter une structure"
      >
        {#snippet links()}
          <TerritoryLink
            label="Voir les thématiques en tension"
            to={autometaUrls.accompagnements}
            openLinkInNewTab
          />
          <TerritoryLink
            label="Vérifier l’existence d’un service"
            to={autometaUrls.services}
            openLinkInNewTab
          />
          <TerritoryLink
            label="Vérifier l’existence d’une structure"
            to={autometaUrls.structures}
            openLinkInNewTab
          />
        {/snippet}
      </TerritoryCard>

      <TerritoryCard
        title="Valoriser mes actions"
        illustration={illuMobiliser}
        to={autometaUrls.accompagnements}
        openLinkInNewTab
        ctaLabel="Voir toutes les statistiques"
      >
        {#snippet links()}
          <TerritoryLink
            label="Adoption et usage"
            to={autometaUrls.accompagnements}
            openLinkInNewTab
          />
          <TerritoryLink
            label="Top orienteurs"
            to={autometaUrls.accompagnements}
            openLinkInNewTab
          />
          <TerritoryLink
            label="Impact des services"
            to={autometaUrls.accompagnements}
            openLinkInNewTab
          />
        {/snippet}
      </TerritoryCard>
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
