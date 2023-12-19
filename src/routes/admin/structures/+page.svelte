<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import AdminDivisionSearch from "$lib/components/inputs/geo/admin-division-search.svelte";
  import { SIREN_POLE_EMPLOI } from "$lib/consts";
  import { CANONICAL_URL } from "$lib/env";
  import { addIcon } from "$lib/icons";
  import { getStructuresAdmin } from "$lib/requests/admin";
  import type { AdminShortStructure, GeoApiValue } from "$lib/types";
  import dayjs from "dayjs";
  import type { PageData } from "./$types";
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
  import * as XLSX from "xlsx";
  import type { StatusFilter } from "./types";

  export let data: PageData;

  let searchStatus: StatusFilter = "toutes";

  let structures: AdminShortStructure[] = [];
  let filteredStructures: AdminShortStructure[] = [];
  let department: GeoApiValue;
  let selectedStructureSlug: string | null = null;

  function filterIgnoredStructures(structs) {
    function isOrphanPoleEmploiStruct(struct) {
      return (
        struct.siret?.slice(0, 9) === SIREN_POLE_EMPLOI && isOrphan(struct)
      );
    }

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
        (!isOrphanPoleEmploiStruct(struct) &&
          !isOrphanOrWaitingOrToActivateSIAE(struct))
    );
  }
  async function handleDepartmentChange(dept: GeoApiValue) {
    department = dept;
    if (department.code) {
      structures = filterIgnoredStructures(
        await getStructuresAdmin(department.code)
      );
    } else {
      structures = [];
    }
  }

  async function handleStructuresRefresh() {
    structures = filterIgnoredStructures(
      await getStructuresAdmin(department.code)
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
      `structures-dora-${department.code}-${searchStatus}-${date}.xlsx`,
      { compression: true }
    );
  }

  if (data.isManager) {
    handleDepartmentChange(data.department);
  }
</script>

{#if !data.isManager && !department}
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

{#if department}
  <CenteredGrid bgColor="bg-service-green">
    <div class="relative gap-s16 lg:flex-row-reverse lg:justify-between">
      <div class="mb-s48 print:mb-s0">
        <Breadcrumb currentLocation="manager-dashboard" dark />
      </div>

      <div>
        <h1 class="mb-s12 mr-s12 text-france-blue">Tableau de bord</h1>
        <div class="flex flex-col justify-between gap-s16 md:flex-row">
          <div
            class=" flex flex-col items-baseline justify-between gap-s8 text-france-blue md:flex-row"
          >
            <span class="text-f23 font-bold"
              >{department.name}({department.code})
            </span>
            <span class="hidden text-f23 font-bold md:block">•</span>
            <a
              href="https://metabase.dora.inclusion.beta.gouv.fr/public/dashboard/860a9da9-9300-4289-878c-7bf8ec74f9b7?d%25C3%25A9partement={department.code}"
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
      servicesOptions={data.servicesOptions}
      structuresOptions={data.structuresOptions}
    />
    <div class="mb-s8 text-gray-text">
      {#if structures?.length !== filteredStructures?.length}
        {filteredStructures.length} structures affichées / {structures.length}
      {:else}
        {structures.length} structures
      {/if}
    </div>
    <div class="flex flex-col gap-s12">
      {#if structures}
        <div class="flex flex-col gap-s16 lg:flex-row">
          <div class="relative h-s512 w-full shrink-0 lg:h-[800px] lg:w-s512">
            <StructuresMap
              {filteredStructures}
              bind:selectedStructureSlug
              {department}
            />
          </div>
          <div class="flex w-full flex-col gap-s24">
            <Button
              on:click={handleClick}
              label="Télécharger"
              secondary
              disabled={!filteredStructures.length}
            />
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
