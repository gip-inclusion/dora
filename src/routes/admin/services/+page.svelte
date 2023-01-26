<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Label from "$lib/components/display/label.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { eyeIcon, homeIcon } from "$lib/icons";
  import { getServicesAdmin } from "$lib/requests/admin";
  import { shortenString } from "$lib/utils/misc";
  import { onMount } from "svelte";

  let services, filteredServices;

  function filterAndSortEntities(searchString) {
    return (
      searchString
        ? services.filter(
            (entity) =>
              entity.name.toLowerCase().includes(searchString) ||
              entity.structureName.toLowerCase().includes(searchString) ||
              entity.structureDept === searchString
          )
        : services
    )
      .filter((entity) => !entity.parent)
      .sort((entity1, entity2) => {
        if (entity1.structureDept !== entity2.structureDept) {
          return entity1.structureDept.localeCompare(
            entity2.structureDept,
            "fr",
            {
              numeric: true,
            }
          );
        }

        if (
          entity1.structureName.toLowerCase() !==
          entity2.structureName.toLowerCase()
        ) {
          return entity1.structureName
            .toLowerCase()
            .localeCompare(entity2.structureName.toLowerCase(), "fr");
        }

        return entity1.name
          .toLowerCase()
          .localeCompare(entity2.name.toLowerCase(), "fr");
      });
  }

  function handleFilterChange(event) {
    const searchString = event.target.value.toLowerCase().trim();
    filteredServices = filterAndSortEntities(searchString);
  }

  onMount(async () => {
    services = await getServicesAdmin();
    filteredServices = filterAndSortEntities("");
  });
</script>

<CenteredGrid>
  <h2>Services</h2>

  <div class="flex flex-col gap-s12">
    <div class="mb-s12 flex w-full flex-row items-center gap-s12">
      <div class="grow">
        <input
          on:input={handleFilterChange}
          class="w-full border border-gray-02 p-s8"
          placeholder="rechercher (nom du service, de sa structure, numéro du département)…"
        />
      </div>
      {#if services?.length !== filteredServices?.length}
        <div class="text-gray-text">
          ({filteredServices.length} / {services.length})
        </div>
      {/if}
    </div>

    {#if services}
      {#each filteredServices as service}
        <div
          class="flex flex-row items-center gap-s16 rounded-md border border-gray-01 bg-white p-s16"
        >
          <div class="flex-auto basis-1/3">
            <a href="/admin/services/{service.slug}" target="_blank">
              <h5 class="mb-s0">{shortenString(service.name)}</h5>
            </a>

            <Label
              label="{service.structureName} ({service.structureDept})"
              smallIcon
              icon={homeIcon}
            />
          </div>
          <div class="flex flex-none basis-1/6 flex-col">
            {#if service.diffusionZoneType !== "country"}
              <Label label={service.diffusionZoneTypeDisplay} />
            {/if}
            <Label label={service.diffusionZoneDetailsDisplay} bold />
          </div>

          <div class="flex-none basis-s32">
            <LinkButton
              to="/services/{service.slug}"
              icon={eyeIcon}
              noBackground
              otherTab
            />
          </div>
        </div>
      {/each}
    {:else}
      Chargement…
    {/if}
  </div>
</CenteredGrid>
