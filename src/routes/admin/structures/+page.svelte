<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import AdminDivisionSearch from "$lib/components/inputs/geo/admin-division-search.svelte";
  import { CANONICAL_URL } from "$lib/env";
  import { getStructuresAdmin } from "$lib/requests/admin";
  import type { AdminShortStructure, GeoApiValue } from "$lib/types";
  import dayjs from "dayjs";
  import type { PageData } from "./$types";
  import Filters from "./filters.svelte";
  import StructuresMap from "./structures-map.svelte";
  import StructuresTable from "./structures-table.svelte";
  import * as XLSX from "xlsx";
  import type { StatusFilter } from "./types";

  export let data: PageData;

  let searchStatus: StatusFilter = "toutes";

  let structures: AdminShortStructure[] = [];
  let filteredStructures: AdminShortStructure[] = [];
  let department: GeoApiValue;
  let selectedStructureSlug: string | null = null;

  function filterOrphanPoleEmploiStructures(structs) {
    return structs.filter(
      (struct) =>
        struct.siret?.slice(0, 9) !== "130005481" ||
        struct.hasAdmin ||
        struct.adminsToRemind.length
    );
  }
  async function handleDepartmentChange(dept: GeoApiValue) {
    department = dept;
    if (department.code) {
      structures = filterOrphanPoleEmploiStructures(
        await getStructuresAdmin(department.code)
      );
    } else {
      structures = [];
    }
  }

  async function handleStructuresRefresh() {
    structures = filterOrphanPoleEmploiStructures(
      await getStructuresAdmin(department.code)
    );
  }

  function handleClick() {
    const sheetData = filteredStructures.map((structure) => {
      let status = "";
      if (structure.isObsolete) {
        status = "obsolète";
      } else if (!structure.hasAdmin && !structure.adminsToRemind.length) {
        status = "orpheline";
      } else if (structure.adminsToRemind.length) {
        status = "en attente";
      } else if (structure.moderationStatus !== "VALIDATED") {
        status = "à modérer";
      } else if (!structure.numPublishedServices) {
        status = "à activer";
      } else if (structure.numOutdatedServices) {
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

<CenteredGrid>
  {#if !data.isManager}
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
  {:else}
    <h1>
      {department.name}({department.code})
    </h1>
  {/if}

  {#if department}
    <div class="my-s24 text-center text-f18 font-bold">
      <a
        href="https://metabase.dora.fabrique.social.gouv.fr/public/dashboard/860a9da9-9300-4289-878c-7bf8ec74f9b7?d%25C3%25A9partement={department.code}"
        target="_blank"
        rel="noopener nofollow"
        class="underline"
      >
        Voir les statistiques
      </a>
    </div>
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
  {/if}
</CenteredGrid>
