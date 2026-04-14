<script lang="ts">
  import EyeLineSystem from "svelte-remix/EyeLineSystem.svelte";
  import Home6LineBuildings from "svelte-remix/Home6LineBuildings.svelte";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Label from "$lib/components/display/label.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { shortenString } from "$lib/utils/misc";
  import { filterAndSortServices } from "$lib/utils/moderation";

  let { data } = $props();

  let services = $state([]);
  let searchString = $state("");
  let filteredServices = $derived(
    filterAndSortServices(services, searchString)
  );

  data.services.then((result) => {
    services = result;
  });

  let debounceTimer: ReturnType<typeof setTimeout>;

  function handleFilterChange(event) {
    const value = event.target.value.toLowerCase().trim();
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      searchString = value;
    }, 300);
  }
</script>

<CenteredGrid>
  <h2>Services</h2>

  <div class="gap-s12 flex flex-col">
    <div class="mb-s12 gap-s12 flex w-full flex-row items-center">
      <div class="grow">
        <input
          oninput={handleFilterChange}
          class="border-gray-02 p-s8 w-full border"
          placeholder="rechercher (nom du service, de sa structure, numéro du département)…"
        />
      </div>
      {#if services?.length !== filteredServices?.length}
        <div class="text-gray-text">
          ({filteredServices.length} / {services.length})
        </div>
      {/if}
    </div>

    {#await data.services}
      Chargement...
    {:then _}
      {#each filteredServices as service}
        <div
          class="gap-s16 border-gray-01 p-s16 flex flex-row items-center rounded-lg border bg-white"
        >
          <div class="flex-auto basis-1/3">
            <a href="/admin/services/{service.slug}" target="_blank">
              <h5 class="mb-s0">{shortenString(service.name)}</h5>
            </a>

            <Label
              label="{service.structureName} ({service.structureDept})"
              smallIcon
              icon={Home6LineBuildings}
            />
          </div>
          <div class="flex flex-none basis-1/6 flex-col">
            {#if service.diffusionZoneType !== "country"}
              <Label label={service.diffusionZoneTypeDisplay} />
            {/if}
            <Label label={service.diffusionZoneDetailsDisplay} bold />
          </div>

          <div class="basis-s32 flex-none">
            <LinkButton
              to="/services/{service.slug}"
              icon={EyeLineSystem}
              noBackground
              otherTab
            />
          </div>
        </div>
      {/each}
    {/await}
  </div>
</CenteredGrid>
