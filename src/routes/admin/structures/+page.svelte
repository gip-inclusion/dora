<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import AdminDivisionSearch from "$lib/components/inputs/geo/admin-division-search.svelte";
  import { getStructuresAdmin } from "$lib/requests/admin";
  import type { AdminShortStructure, GeoApiValue } from "$lib/types";
  import type { PageData } from "./$types";
  import Filters from "./filters.svelte";
  import StructuresMap from "./structures-map.svelte";
  import StructuresTable from "./structures-table.svelte";

  export let data: PageData;
  let structures: AdminShortStructure[] = [];
  let filteredStructures: AdminShortStructure[] = [];
  let department: GeoApiValue;
  let selectedStructureSlug: string | null = null;

  async function handleDepartmentChange(dept: GeoApiValue) {
    department = dept;
    if (department.code) {
      structures = await getStructuresAdmin(department.code);
    } else {
      structures = [];
    }
  }
</script>

<CenteredGrid>
  <h2>Structures</h2>

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

  {#if department}
    <div class="my-s32 flex flex-row justify-evenly gap-s24">
      <div
        class="flex max-w-fit flex-col rounded border border-gray-01 p-s16 text-center"
      >
        <div class="text-bold text-f24 text-france-blue">
          Nb de structures orphelines
        </div>
        <div class="text-bold text-f38 text-france-blue">XXX</div>
      </div>

      <div
        class="flex max-w-fit flex-col rounded border border-gray-01 p-s16 text-center"
      >
        <div class="text-bold text-f24 text-france-blue">
          Nombre de services publiés
        </div>
        <div class="text-bold text-f38 text-france-blue">XXX</div>
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
              servicesOptions={data.servicesOptions}
              bind:selectedStructureSlug
            />
          </div>
        </div>
      {:else}
        Chargement…
      {/if}
    </div>
  {/if}
</CenteredGrid>
