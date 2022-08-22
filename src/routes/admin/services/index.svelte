<script>
  import { onMount } from "svelte";
  import { getServicesAdmin } from "$lib/admin";

  import { shortenString } from "$lib/utils";
  import { eyeIcon, homeIcon } from "$lib/icons";
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  let services, filteredServices;

  onMount(async () => {
    services = await getServicesAdmin();
    filteredServices = filterAndSortEntities("");
  });

  function filterAndSortEntities(searchString) {
    return (
      searchString
        ? services.filter(
            (s) =>
              s.name.toLowerCase().includes(searchString) ||
              s.structureName.toLowerCase().includes(searchString) ||
              s.structureDept === searchString
          )
        : services
    )
      .filter((s) => !s.parent)
      .sort((s1, s2) => {
        if (s1.structureDept !== s2.structureDept) {
          return s1.structureDept.localeCompare(s2.structureDept, "fr", {
            numeric: true,
          });
        }

        if (s1.structureName.toLowerCase() !== s2.structureName.toLowerCase()) {
          return s1.structureName
            .toLowerCase()
            .localeCompare(s2.structureName.toLowerCase(), "fr");
        }

        return s1.name.toLowerCase().localeCompare(s2.name.toLowerCase(), "fr");
      });
  }

  function handleFilterChange(event) {
    const searchString = event.target.value.toLowerCase().trim();
    filteredServices = filterAndSortEntities(searchString);
  }
</script>

<svelte:head>
  <title>Admin | Services | DORA</title>
</svelte:head>

<CenteredGrid bgColor="bg-gray-bg">
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
          class="flex flex-row items-center gap-s16 rounded-md bg-white p-s16"
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
