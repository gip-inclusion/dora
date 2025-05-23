<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import AdminDivisionSearch from "$lib/components/inputs/geo/admin-division-search.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import { CANONICAL_URL } from "$lib/env";
  import { addIcon } from "$lib/icons";
  import { getStructuresAdmin } from "$lib/requests/admin";
  import type { AdminShortStructure, GeoApiValue } from "$lib/types";
  import dayjs from "dayjs";
  import type { PageData } from "./$types";
  import Filters from "./filters.svelte";
  import StructuresMap from "./structures-map.svelte";
  import StructuresTable from "./structures-table.svelte";
  import DepartmentList from "./department-list.svelte";
  import {
    isOrphan,
    toActivate,
    waiting,
    isObsolete,
    toUpdate,
    toModerate,
  } from "./structures-filters";
  import * as XLSX from "xlsx";
  import type { StatusFilter } from "./types";

  export let data: PageData;

  let selectedDepartment = data.department;
  let searchStatus: StatusFilter = "toutes";
  let filterDefinition: string | undefined;
  let filterActions: string | undefined;
  let structures: AdminShortStructure[] = [];
  let filteredStructures: AdminShortStructure[] = [];
  let selectedStructureSlug: string | null = null;
  let loading = false;

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
      await getStructuresAdmin(selectedDepartment.code)
    );
  }

  function handleClick() {
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

    const worksheet = XLSX.utils.json_to_sheet(sheetData);
    worksheet["!cols"] = Array(18).fill({ wch: 20 });
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet);
    const date = dayjs().format("YYYY-MM-DD");
    XLSX.writeFile(
      workbook,
      `structures-dora-${selectedDepartment.code}-${searchStatus}-${date}.xlsx`,
      { compression: true }
    );
  }

  if (data.isManager) {
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
        withGeom
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

            <a
              href="https://metabase.dora.inclusion.beta.gouv.fr/public/dashboard/860a9da9-9300-4289-878c-7bf8ec74f9b7?d%25C3%25A9partement={selectedDepartment.code}"
              target="_blank"
              rel="noopener nofollow"
              class="text-f18 underline"
            >
              Voir les statistiques
            </a>
          </div>

          <div>
            <LinkButton
              label="Ajouter une structure"
              to="/admin/structures/creer"
              icon={addIcon}
            />
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
            <StructuresMap
              {filteredStructures}
              bind:selectedStructureSlug
              department={selectedDepartment}
            />
          </div>
          <div class="gap-s24 flex w-full flex-col">
            <Button
              on:click={handleClick}
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
                    href="https://aide.dora.inclusion.beta.gouv.fr/fr/article/comment-utiliser-le-tableau-de-bord-de-gestionnaire-de-territoire-b5do49/"
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
