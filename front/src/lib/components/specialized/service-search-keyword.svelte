<script lang="ts">
  import insane from "insane";

  import DeleteBack2FillSystem from "svelte-remix/DeleteBack2FillSystem.svelte";
  import MapPin2LineMap from "svelte-remix/MapPin2LineMap.svelte";
  import SearchLineSystem from "svelte-remix/SearchLineSystem.svelte";

  import { goto } from "$app/navigation";

  import Button from "$lib/components/display/button.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import { LocationType } from "$lib/consts";
  import { getDepartmentFromCityCode } from "$lib/utils/misc";
  import { search as searchBAN } from "$lib/requests/ban";
  import type { BANFeature } from "$lib/requests/ban";
  import {
    searchDepartment,
    searchRegion,
  } from "$lib/utils/service-search-keyword";

  interface AddressResult {
    kind: LocationType;
    label: string;
    searchParams: URLSearchParams;
  }

  let address: AddressResult | null = null;
  let addressQuery = $state("");
  let selectErrors = $state([]);
  let serviceQuery = $state("");

  let isLoading = $state(false);
  let submitDisabled = $derived(!addressQuery && !serviceQuery);

  async function searchAddress(addrQuery: string) {
    const addresses = [];
    const cities = [];
    let banData: BANFeature[];
    try {
      banData = await searchBAN(addrQuery);
      selectErrors = [];
    } catch {
      banData = [];
      selectErrors = ["Impossible de contacter la Base Adresse Nationale."];
    }
    banData.forEach((feature) => {
      if (feature.properties.type === "municipality") {
        const label = `${feature.properties.city} (${getDepartmentFromCityCode(
          feature.properties.citycode
        )})`;
        cities.push({
          value: {
            kind: LocationType.City,
            label,
            searchParams: new URLSearchParams({
              code_commune: feature.properties.citycode,
            }),
          },
          label,
        });
      } else {
        const [lat, lon] = feature.geometry.coordinates;
        addresses.push({
          value: {
            searchParams: new URLSearchParams({
              lat: lat.toString(),
              lon: lon.toString(),
            }),
            kind: LocationType.Address,
            label: feature.properties.label,
          },
          label: feature.properties.label,
        });
      }
    });

    const results: AddressResult[] = [];
    if (cities.length) {
      results.push(cities[0]);
    }
    const department = searchDepartment(addrQuery);
    if (department) {
      const label = `${department.label} (${department.code})`;
      results.push({
        value: {
          label,
          kind: LocationType.Department,
          searchParams: new URLSearchParams({
            code_departement: department.code,
          }),
        },
        label,
      });
    }
    const region = searchRegion(addrQuery);
    if (region) {
      results.push({
        value: {
          label: region.label,
          kind: LocationType.Region,
          searchParams: new URLSearchParams({
            code_region: region.code,
          }),
        },
        label: region.label,
      });
    }
    results.push(...addresses.slice(0, 10 - results.length));
    return results;
  }

  function handleAddressChange(newAddress) {
    if (newAddress) {
      addressQuery = newAddress.label;
      address = newAddress;
    } else {
      addressQuery = "";
      address = null;
    }
  }

  async function handleSearch(event: Event) {
    event.preventDefault();
    isLoading = true;
    await goto(`/recherche-mot-cles?${serviceQuery}`, { noScroll: true });
    isLoading = false;
  }
</script>

<form onsubmit={handleSearch}>
  <div class="border-gray-02 w-full rounded-lg border bg-white">
    <div class="grid">
      <div
        class="city border-gray-02 p-s16 text-f14 flex items-center border-b lg:border-r lg:border-b-0"
      >
        <div class="mr-s8 h-s24 w-s24 text-magenta-cta fill-current">
          <MapPin2LineMap />
        </div>
        <div class="relative w-full">
          <label class="sr-only" for="place">
            Lieu
            <span class="text-error">*</span>
          </label>
          {#snippet itemContent({ item })}
            <span>
              {@html insane(item.highlighted.label, {
                allowedTags: ["b"],
              })}
              <span class="text-slate-100 TODO NOT WORKING">
                {#if item.value.kind === LocationType.Department}
                  - département
                {:else if item.value.kind === LocationType.Region}
                  - région
                {/if}
              </span>
            </span>
          {/snippet}
          <Select
            id="place"
            minCharactersToSearch="4"
            bind:searchText={addressQuery}
            onChange={handleAddressChange}
            searchFunction={searchAddress}
            delay="200"
            localFiltering={false}
            hideArrow
            placeholder="Lieu ; exemple : 1 rue de l’Espoir 33000 Bordeaux"
            {selectErrors}
            {itemContent}
          />
          <div
            class="right-s12 top-s12 h-s24 w-s24 text-gray-dark absolute z-10"
          >
            {#if addressQuery}
              <button
                class="h-s24 w-s24 inline-block"
                onclick={() => {
                  handleAddressChange(null);
                }}
              >
                <span class="h-s24 w-s24 text-gray-text-alt fill-current">
                  <DeleteBack2FillSystem />
                </span>
                <span class="sr-only">Supprimer la ville sélectionnée</span>
              </button>
            {/if}
          </div>
        </div>
      </div>

      <div
        class="border-gray-02 px-s16 py-s24 text-f14 lg:py-s16 flex border-b lg:border-r lg:border-b-0"
      >
        <div
          class="mr-s8 h-s24 w-s24 text-magenta-cta self-center fill-current"
        >
          <SearchLineSystem />
        </div>

        <label for="searchterm" class="sr-only">Mots-clés</label>
        <input
          bind:value={serviceQuery}
          id="searchterm"
          class="w-full px-s16"
          placeholder="Type de structure, thématique, public, mot-clé…"
        />
      </div>

      <div class="p-s12 lg:p-s16 text-center">
        <Button
          type="submit"
          label="Rechercher"
          title={submitDisabled
            ? "Modifiez un des critères avant d’actualiser la recherche"
            : undefined}
          disabled={submitDisabled}
          loading={isLoading}
        />
      </div>
    </div>
  </div>
</form>

<style lang="postcss">
  @reference "../../../app.css";

  .grid {
    grid-template-columns: 1fr;
    display: grid;
  }
  @media (width >= 64rem) {
    .grid {
      grid-template-columns: 3fr 3fr 1fr;
    }
  }

  .grid :global(.autocomplete-input) {
    @apply border-0;
  }
  .grid :global(.city .autocomplete) {
    @apply block;
  }
  .grid :global(.input-container input) {
    @apply bg-transparent;
  }
  .grid :global(input::placeholder) {
    @apply text-gray-text;
  }
</style>
