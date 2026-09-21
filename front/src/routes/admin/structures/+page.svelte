<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/state";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import { URL_MANAGER_DASHBOARD_HELP_NOTICE } from "$lib/consts";
  import { CANONICAL_URL } from "$lib/env";
  import { getStructuresAdmin } from "$lib/requests/admin";
  import type { AdminStructure, GeoApiValue } from "$lib/types";
  import { saveLastDepartment } from "$lib/utils/manager-department";

  import DepartmentSelector from "$lib/components/specialized/department-selector.svelte";

  import type { PageData } from "./$types";
  import Filters from "./filters.svelte";
  import StructuresMap from "./structures-map.svelte";
  import StructuresTable from "./structures-table.svelte";
  import {
    getStatusDefinition,
    getStructureStatus,
    getStatusLabel,
    parseStatusFilter,
  } from "./structures-filters";
  import type { StatusFilter } from "./types";
  import { generateSpreadsheet } from "$lib/utils/spreadsheet";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  let selectedDepartment = $state(data.department);
  // Correspondance entre le paramètre d'URL `statut` et le filtre basé sur le statut correspondant.
  const searchStatus = $derived(
    parseStatusFilter(page.url.searchParams.get("statut"))
  );

  function setSearchStatus(status: StatusFilter) {
    const url = new URL(page.url);
    if (status === "all") {
      url.searchParams.delete("statut");
    } else {
      url.searchParams.set("statut", status);
    }
    goto(url, { replaceState: true, keepFocus: true, noScroll: true });
  }
  let structures: AdminStructure[] = $state([]);
  let filteredStructures: AdminStructure[] = $state([]);
  let selectedStructureSlug: string | null = $state(null);
  let loading = $state(false);

  const filterDefinition = $derived(getStatusDefinition(searchStatus));

  async function handleDepartmentChange(dept: GeoApiValue) {
    structures = [];
    loading = true;
    selectedDepartment = dept;
    saveLastDepartment(dept);
    structures = await getStructuresAdmin(dept.code);
    loading = false;
  }

  async function handleStructuresRefresh() {
    structures = await getStructuresAdmin(selectedDepartment?.code);
  }

  // Exporte la liste entière des structures du territoire, sans tenir compte
  // des filtres actifs.
  function handleDownload() {
    if (!selectedDepartment || !structures?.length) {
      return;
    }

    const sheetData = structures.map((structure) => {
      const structStatus = getStructureStatus(structure);
      const status = getStatusLabel(structStatus);

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
        "Invitation envoyée": structure.adminAlreadyInvited ? "oui" : "non",
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
      sheetName: `structures-dora-${selectedDepartment.code}`,
    });
  }

  handleDepartmentChange(data.department);
</script>

{#if selectedDepartment}
  <CenteredGrid>
    <div class="mb-s32">
      <Breadcrumb currentLocation="manager-dashboard" />
    </div>

    <div class="gap-s16 mb-s48 flex flex-col justify-between md:flex-row">
      <div>
        <h1 class="mb-s8 text-france-blue">Mes structures & services Dora</h1>

        <div class="text-france-blue">
          {#if data.departments?.length > 1}
            <DepartmentSelector
              departments={data.departments}
              {selectedDepartment}
              onChange={handleDepartmentChange}
            />
          {:else}
            <span class="text-f23 font-bold">
              {selectedDepartment.name} ({selectedDepartment.code})
            </span>
          {/if}
        </div>
      </div>

      <div class="gap-s16 flex shrink-0 flex-wrap items-start">
        <LinkButton
          label="Notice"
          to={URL_MANAGER_DASHBOARD_HELP_NOTICE}
          otherTab
          nofollow
          secondary
        />
        <Button
          onclick={handleDownload}
          label="Télécharger la liste (xlsx)"
          disabled={loading || !structures?.length}
        />
      </div>
    </div>

    <Filters
      {structures}
      bind:filteredStructures
      bind:searchStatus={() => searchStatus, setSearchStatus}
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
            {#if searchStatus !== "all" && filterDefinition}
              <Notice type="info" title={filterDefinition}>
                <div>
                  <a
                    href={URL_MANAGER_DASHBOARD_HELP_NOTICE}
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
