<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import AdminDivisionSearch from "$lib/components/inputs/geo/admin-division-search.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import {
    DI_METABASE_LIST_DASHBOARD_URL,
    DI_METABASE_STATS_DASHBOARD_URL,
    METABASE_DASHBOARD_URL,
    URL_HELP_SITE,
  } from "$lib/consts";
  import { CANONICAL_URL } from "$lib/env";
  import AddFillSystem from "svelte-remix/AddFillSystem.svelte";
  import { getStructuresAdmin } from "$lib/requests/admin";
  import type { AdminShortStructure, GeoApiValue } from "$lib/types";

  import type { PageData } from "./$types";
  import DepartmentList from "./department-list.svelte";
  import Filters from "./filters.svelte";
  import StructuresMap from "./structures-map.svelte";
  import StructuresTable from "./structures-table.svelte";
  import {
    isOrphan,
    toActivate,
    waiting,
    isObsolete,
    toUpdate,
    toModerate,
  } from "./structures-filters";
  import type { StatusFilter } from "./types";
  import { generateSpreadsheet } from "$lib/utils/spreadsheet";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  let selectedDepartment = $state(data.department);
  let searchStatus: StatusFilter = $state("toutes");
  let filterDefinition: string | undefined = $state();
  let filterActions: string | undefined = $state();
  let structures: AdminShortStructure[] = $state([]);
  let filteredStructures: AdminShortStructure[] = $state([]);
  let selectedStructureSlug: string | null = $state(null);
  let loading = $state(false);

  function filterIgnoredStructures(structs) {
    function isOrphanOrWaitingOrToActivateSIAE(struct) {
      return (
        ["ETTI", "ACI", "AI", "EI"].includes(struct.typology) &&
        (isOrphan(struct) || waiting(struct) || toActivate(struct))
      );
    }

    return structs.filter(
      (struct) =>
        isObsolete(struct) ||
        toModerate(struct) ||
        !isOrphanOrWaitingOrToActivateSIAE(struct)
    );
  }

  async function handleDepartmentChange(dept: GeoApiValue) {
    structures = [];
    loading = true;
    selectedDepartment = dept;
    if (selectedDepartment.code) {
      structures = filterIgnoredStructures(
        await getStructuresAdmin(selectedDepartment.code)
      );
    } else {
      structures = [];
    }
    loading = false;
  }

  async function handleStructuresRefresh() {
    structures = filterIgnoredStructures(
      await getStructuresAdmin(selectedDepartment?.code)
    );
  }

  function handleClick() {
    if (!selectedDepartment) {
      return;
    }

    const sheetData = filteredStructures.map((structure) => {
      let status = "";
      if (isObsolete(structure)) {
        status = "obsolète";
      } else if (isOrphan(structure)) {
        status = "orpheline";
      } else if (waiting(structure)) {
        status = "en attente";
      } else if (toModerate(structure)) {
        status = "à modérer";
      } else if (toActivate(structure)) {
        status = "à activer";
      } else if (toUpdate(structure)) {
        status = "à actualiser";
      }

      // prettier-ignore
      return {
        "Nom": structure.name,
        "SIRET": structure.siret,
        "Département": structure.department,
        "Ville": structure.city,
        "Description": structure.shortDesc,
        "Thématiques": structure.categories
          .map(
            (val) =>
              data.servicesOptions?.categories.find((cat) => cat.value === val)
                ?.label
          )
          .filter(value => !!value)
          .join(", "),
        "Téléphone": structure.phone,
        "Courriel": structure.email,
        "Lien DORA": `${CANONICAL_URL}/structures/${structure.slug}`,
        "Administrateurs": structure.admins.join(","),
        "Éditeurs": structure.editors.join(","),
        "Administrateur déjà invité": structure.adminAlreadyInvited ? "oui" : "non",
        "Administrateurs à relancer": structure.adminsToRemind.join(","),
        "Administrateurs à modérer": structure.adminsToModerate.join(","),
        "Collaborateurs à relancer": structure.numPotentialMembersToRemind,
        "Collaborateurs en attente": structure.numPotentialMembersToValidate,
        "Nb services publiés": structure.numPublishedServices,
        "Nb services à maj": structure.numOutdatedServices,
        "Nb services brouillon": structure.numDraftServices,
        "Statut": status,
      };
    });

    generateSpreadsheet({
      sheetData,
      sheetName: `structures-dora-${selectedDepartment.code}-${searchStatus}`,
    });
  }

  if (data.isManager && data.department) {
    handleDepartmentChange(data.department);
  }
</script>

{#if !data.isManager && !selectedDepartment}
  <CenteredGrid>
    <div class="mb-s16 flex flex-col">
      <label for="department" class="font-bold">Département</label>
      <AdminDivisionSearch
        id="department"
        searchType="department"
        onChange={handleDepartmentChange}
        placeholder="numéro ou nom"
      />
    </div>
  </CenteredGrid>
{/if}

{#if selectedDepartment}
  <CenteredGrid bgColor="bg-service-green">
    <div class="gap-s16 relative lg:flex-row-reverse lg:justify-between">
      <div class="mb-s48 print:mb-s0">
        <Breadcrumb currentLocation="manager-dashboard" />
      </div>

      <div>
        <h1 class="mb-s12 mr-s12 text-france-blue">Tableau de bord</h1>
        <div class="gap-s16 flex flex-col justify-between md:flex-row">
          <div
            class="gap-s24 text-france-blue flex flex-col items-baseline justify-between md:flex-row"
          >
            {#if data.departments?.length > 1}
              <DepartmentList
                departments={data.departments}
                {selectedDepartment}
                onRefresh={handleDepartmentChange}
              />
            {:else}
              <span class="text-f23 font-bold">
                {selectedDepartment.name}({selectedDepartment.code})
              </span>
              <span class="text-f23 hidden font-bold md:block">•</span>
            {/if}
          </div>

          <div class="flex flex-col items-end">
            <LinkButton
              label="Ajouter une structure"
              to="/admin/structures/creer"
              icon={AddFillSystem}
              extraClass="mb-s12"
            />
            <a
              href={DI_METABASE_STATS_DASHBOARD_URL(selectedDepartment.name)}
              target="_blank"
              rel="noopener nofollow"
              class="text-f18 text-france-blue leading-32 underline"
            >
              Cartographie des structures et services référencés
            </a>
            <a
              href={DI_METABASE_LIST_DASHBOARD_URL(selectedDepartment.name)}
              target="_blank"
              rel="noopener nofollow"
              class="text-f18 text-france-blue leading-32 underline"
            >
              Liste des structures et services référencés
            </a>
            <a
              href={METABASE_DASHBOARD_URL(selectedDepartment.code)}
              target="_blank"
              rel="noopener nofollow"
              class="text-f18 text-france-blue leading-32 underline"
            >
              Statistiques d’utilisation de mon territoire
            </a>
          </div>
        </div>
      </div>
    </div>
  </CenteredGrid>
  <CenteredGrid>
    <Filters
      {structures}
      bind:filteredStructures
      bind:searchStatus
      bind:filterDefinition
      bind:filterActions
      servicesOptions={data.servicesOptions}
      structuresOptions={data.structuresOptions}
    />

    <div class="mb-s8 text-gray-text">
      {#if loading}
        <strong>Chargement en cours…</strong>
      {:else if structures?.length !== filteredStructures?.length}
        {filteredStructures.length} structures affichées / {structures.length}
      {:else}
        {structures.length} structures
      {/if}
    </div>
    <div class="gap-s12 flex flex-col">
      {#if structures}
        <div class="gap-s16 flex flex-col lg:flex-row">
          <div class="h-s512 lg:w-s512 relative w-full shrink-0 lg:h-[800px]">
            <StructuresMap {filteredStructures} bind:selectedStructureSlug />
          </div>
          <div class="gap-s24 flex w-full flex-col">
            <Button
              onclick={handleClick}
              label="Télécharger"
              secondary
              disabled={!filteredStructures.length}
            />
            {#if searchStatus !== "toutes" && filterDefinition}
              <Notice type="info" title={filterDefinition}>
                <div>
                  {#if filterActions}
                    Action(s)&#8239;: {filterActions}
                  {/if}
                  <a
                    href={`${URL_HELP_SITE}article/comment-utiliser-le-tableau-de-bord-de-gestionnaire-de-territoire-b5do49/`}
                    target="_blank"
                    class="text-magenta-cta underline"
                  >
                    Mode d’emploi détaillé
                  </a>
                </div>
              </Notice>
            {/if}
            <StructuresTable
              {filteredStructures}
              bind:selectedStructureSlug
              onRefresh={handleStructuresRefresh}
            />
          </div>
        </div>
      {:else}
        Chargement…
      {/if}
    </div>
  </CenteredGrid>
{/if}
