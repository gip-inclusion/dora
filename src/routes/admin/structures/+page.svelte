<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import AdminDivisionSearch from "$lib/components/inputs/geo/admin-division-search.svelte";
  import { getStructuresAdmin } from "$lib/requests/admin";
  import type { AdminShortStructure, GeoApiValue } from "$lib/types";
  import type { PageData } from "./$types";
  import Filters from "./filters.svelte";
  import StructuresMap from "./structures-map.svelte";
  import StructuresTable from "./structures-table.svelte";
  import { fetchData } from "$lib/utils/misc";
  import { getApiURL } from "$lib/utils/api";

  export let data: PageData;

  interface AdminStats {
    nbActiveStructs: number;
    nbOrphanStructs: number;
    nbPublishedServices: number;
    nbUsers: number;
  }

  let structures: AdminShortStructure[] = [];
  let stats: AdminStats | null;
  let filteredStructures: AdminShortStructure[] = [];
  let department: GeoApiValue;
  let selectedStructureSlug: string | null = null;

  async function getStats(dept: string) {
    const url = `${getApiURL()}/admin-stats/?department=${dept}`;
    return (await fetchData<AdminStats>(url)).data;
  }

  async function handleDepartmentChange(dept: GeoApiValue) {
    department = dept;
    if (department.code) {
      structures = await getStructuresAdmin(department.code);
      stats = await getStats(department.code);
    } else {
      structures = [];
    }
  }

  async function handleStructuresRefresh() {
    structures = await getStructuresAdmin(department.code);
  }

  if (data.isLocalCoordinator) {
    handleDepartmentChange(data.department);
  }
</script>

<CenteredGrid>
  {#if !data.isLocalCoordinator}
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
    <div class="my-s32 flex flex-row flex-wrap justify-between gap-s24">
      <div
        class="flex  flex-1 flex-col  justify-between rounded border border-gray-01 p-s16 text-center"
      >
        <div class="text-bold text-f16 text-france-blue">
          Nb de structures actives
        </div>
        <div class="text-bold text-f24 text-france-blue">
          {stats?.nbActiveStructs || "–"}
        </div>
      </div>

      <div
        class="flex  flex-1  flex-col justify-between rounded border  border-gray-01 p-s16 text-center"
      >
        <div class="text-bold text-f16 text-france-blue">
          Nb de structures orphelines
        </div>
        <div class="text-bold text-f24 text-france-blue">
          {stats?.nbOrphanStructs || "–"}
        </div>
      </div>

      <div
        class="flex  flex-1  flex-col justify-between rounded border border-gray-01 p-s16 text-center"
      >
        <div class="text-bold text-f16 text-france-blue">
          Nombre de services publiés
        </div>
        <div class="text-bold text-f24 text-france-blue">
          {stats?.nbPublishedServices || "–"}
        </div>
      </div>

      <div
        class="flex  flex-1  flex-col justify-between rounded border border-gray-01 p-s16 text-center"
      >
        <div class="text-bold text-f16 text-france-blue">
          Nombre d’utilisateurs
        </div>
        <div class="text-bold text-f24 text-france-blue">
          {stats?.nbUsers || "–"}
        </div>
      </div>
    </div>
    <Filters
      {structures}
      bind:filteredStructures
      servicesOptions={data.servicesOptions}
      structuresOptions={data.structuresOptions}
    />
    {#if structures?.length !== filteredStructures?.length}
      <div class="text-gray-text">
        ({filteredStructures.length} / {structures.length})
      </div>
    {/if}

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
          <div>
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
