<script lang="ts">
  import illuAccompagner from "$lib/assets/illustrations/illu-accompagner.svg";
  import illuMobiliser from "$lib/assets/illustrations/illu-mobiliser.svg";
  import illuRecenser from "$lib/assets/illustrations/illu-recenser.svg";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import DepartmentSelector from "$lib/components/specialized/department-selector.svelte";

  import {
    AUTOMETA_MANAGER_DASHBOARD_URLS,
    URL_MANAGER_HELP_NOTICE,
  } from "$lib/consts";
  import { getStructuresAdmin } from "$lib/requests/admin";
  import type { AdminStructure, GeoApiValue } from "$lib/types";
  import { logException } from "$lib/utils/logger";
  import { saveLastDepartment } from "$lib/utils/manager-department";

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
  let loadingError = $state(false);

  // Identifie la dernière requête afin d'éviter d'afficher les résultats
  // d'une requête plus ancienne.
  let currentRequestId = 0;

  const autometaUrls = $derived(
    AUTOMETA_MANAGER_DASHBOARD_URLS(selectedDepartment.code)
  );

  // Mêmes calculs que les filtres du tableau de bord (/admin/structures)
  // afin que les compteurs coïncident entre les deux pages.
  const counters = $derived.by(() => {
    if (!structures) {
      return null;
    }

    const counts = {
      awaitingActivation: 0,
      awaitingModeration: 0,
      awaitingUpdate: 0,
    };

    for (const structure of structures) {
      const status = getStructureStatus(structure);
      if (status && status in counts) {
        counts[status as keyof typeof counts] += 1;
      }
    }

    return counts;
  });

  async function loadDepartment(department: GeoApiValue) {
    const requestId = ++currentRequestId;

    selectedDepartment = department;
    saveLastDepartment(department);
    structures = null;
    loading = true;
    loadingError = false;

    try {
      const results = await getStructuresAdmin(department.code);

      if (requestId !== currentRequestId) {
        return;
      }

      structures = results ?? null;
      loadingError = !results;
    } catch (err) {
      if (requestId === currentRequestId) {
        logException(err);
        loadingError = true;
      }
    } finally {
      if (requestId === currentRequestId) {
        loading = false;
      }
    }
  }

  loadDepartment(data.department);
</script>

<CenteredGrid>
  <div class="mb-s32">
    <Breadcrumb currentLocation="manager-homepage" />
  </div>

  <div class="gap-s16 mb-s48 flex flex-col justify-between md:flex-row">
    <div>
      <h1 class="mb-s8 text-france-blue">Gérer mon territoire</h1>

      <div class="text-france-blue">
        <DepartmentSelector
          departments={data.departments}
          {selectedDepartment}
          onChange={loadDepartment}
        />
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

  {#if loadingError}
    <div class="mb-s32">
      <Notice
        type="error"
        title="Impossible de récupérer les données des structures"
      >
        <p class="text-f14 mb-s0">
          Les informations des structures du département sélectionné ne peuvent
          pas être affichées. Veuillez réessayer plus tard.
        </p>
      </Notice>
    </div>
  {/if}

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
          count={counters?.awaitingActivation}
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
          count={counters?.awaitingUpdate}
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
          to={`${autometaUrls.accompagnements}#section-thematiques`}
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
          to={`${autometaUrls.accompagnements}#section-utilisateurs`}
          openLinkInNewTab
        />
        <TerritoryLink
          label="Top orienteurs"
          to={`${autometaUrls.accompagnements}#section-orienteurs`}
          openLinkInNewTab
        />
        <TerritoryLink
          label="Impact des services"
          to={`${autometaUrls.accompagnements}#section-par-service`}
          openLinkInNewTab
        />
      {/snippet}
    </TerritoryCard>
  </div>
</CenteredGrid>
