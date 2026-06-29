<script lang="ts">
  import insane from "insane";
  import { onMount } from "svelte";

  import DeleteBack2FillSystem from "svelte-remix/DeleteBack2FillSystem.svelte";
  import MapPin2LineMap from "svelte-remix/MapPin2LineMap.svelte";
  import SearchLineSystem from "svelte-remix/SearchLineSystem.svelte";

  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  import Button from "$lib/components/display/button.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import {
    LocationType,
    TEXT_SEARCH_LAST_LOCATION_STORAGE_KEY,
  } from "$lib/consts";
  import { getDepartmentFromCityCode } from "$lib/utils/misc";
  import { search as searchBAN } from "$lib/requests/ban";
  import type { BANFeature } from "$lib/requests/ban";
  import { searchDepartment, searchRegion } from "$lib/utils/search-area";

  interface AddressResult {
    kind: LocationType;
    label: string;
    searchParams: URLSearchParams;
  }

  interface SelectOption {
    value: AddressResult;
    label: string;
  }

  const minCharactersToTriggerSearch = 4;
  const MAX_QUERY_LENGTH = 40;

  let addressSelected: AddressResult | null = $state(null);
  let addressFieldValue = $state("");
  let addressSelectErrorMessages: string[] = $state([]);
  // Conserve la recherche en cours à l'affichage des résultats : on initialise
  // le champ avec le paramètre `q` présent dans l'URL.
  let searchQuery = $state($page.url.searchParams.get("q") ?? "");

  let isLoading = $state(false);
  const submitDisabled = $derived(!addressSelected && !searchQuery);

  async function searchAddress(addrQuery: string) {
    const addresses: SelectOption[] = [];
    const cities: SelectOption[] = [];
    let banData: BANFeature[];
    try {
      addressSelectErrorMessages = [];
      banData = await searchBAN(addrQuery);
    } catch {
      addressSelectErrorMessages = [
        "Impossible d’effectuer une recherche d’adresse. Veuillez réessayer ultérieurement.",
      ];
      banData = [];
    }
    for (const feature of banData) {
      if (feature.properties.type === "municipality") {
        const label = `${feature.properties.city} (${getDepartmentFromCityCode(
          feature.properties.citycode
        )})`;
        cities.push({
          value: {
            kind: LocationType.City,
            label,
            searchParams: new URLSearchParams({
              // eslint-disable-next-line camelcase
              code_commune: feature.properties.citycode,
            }),
          },
          label,
        });
      } else {
        const [lon, lat] = feature.geometry.coordinates;
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
    }

    const results: SelectOption[] = [];
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
            // eslint-disable-next-line camelcase
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
            // eslint-disable-next-line camelcase
            code_region: region.code,
          }),
        },
        label: region.label,
      });
    }
    results.push(...addresses.slice(0, 10 - results.length));
    return results;
  }

  function loadLastLocation(): AddressResult | null {
    try {
      const stored = localStorage.getItem(
        TEXT_SEARCH_LAST_LOCATION_STORAGE_KEY
      );
      if (!stored) {
        return null;
      }
      const parsed = JSON.parse(stored);
      return {
        kind: parsed.kind,
        label: parsed.label,
        searchParams: new URLSearchParams(parsed.searchParams),
      };
    } catch {
      return null;
    }
  }

  function handleAddressChange(newAddress: AddressResult | null) {
    if (newAddress) {
      addressFieldValue = newAddress.label;
      addressSelected = newAddress;
      try {
        localStorage.setItem(
          TEXT_SEARCH_LAST_LOCATION_STORAGE_KEY,
          JSON.stringify({
            kind: newAddress.kind,
            label: newAddress.label,
            searchParams: newAddress.searchParams.toString(),
          })
        );
      } catch {
        // Le localStorage peut être inaccessible.
      }
    } else {
      addressFieldValue = "";
      addressSelected = null;
      localStorage.removeItem(TEXT_SEARCH_LAST_LOCATION_STORAGE_KEY); // On efface le dernier emplacement géographique stocké.
    }
  }

  async function handleSearch(event: Event) {
    event.preventDefault();
    isLoading = true;
    const params = new URLSearchParams();
    if (searchQuery) {
      params.append("q", searchQuery);
    }
    if (addressSelected) {
      for (const [key, value] of addressSelected.searchParams.entries()) {
        params.append(key, value);
      }
    }
    await goto(`/recherche-mots-cles?${params.toString()}`, {
      noScroll: true,
    });

    isLoading = false;
  }

  onMount(() => {
    const lastLocation = loadLastLocation();
    if (lastLocation) {
      addressSelected = lastLocation;
      addressFieldValue = lastLocation.label;
    }
  });
</script>

<form onsubmit={handleSearch}>
  <div class="border-gray-02 w-full rounded-lg border bg-white">
    <div class="grid">
      <div
        class="border-gray-02 p-s16 text-f14 flex items-center border-b lg:border-r lg:border-b-0"
      >
        <div class="mr-s8 h-s24 w-s24 text-magenta-cta fill-current">
          <MapPin2LineMap />
        </div>
        <div class="relative w-full">
          <label class="sr-only" for="place">
            Lieu (tapez au moins {minCharactersToTriggerSearch} caractères pour rechercher)
          </label>
          {#snippet itemContent({ item })}
            <span>
              {@html insane(item.highlighted?.label ?? item.label, {
                allowedTags: ["b"],
              })}
              <span class="text-gray-text-alt2">
                {#if item.value.kind === LocationType.City}
                  · Commune
                {:else if item.value.kind === LocationType.Department}
                  · Département
                {:else if item.value.kind === LocationType.Region}
                  · Région
                {/if}
              </span>
            </span>
          {/snippet}
          <Select
            id="place"
            minCharactersToSearch={minCharactersToTriggerSearch}
            bind:searchText={addressFieldValue}
            onChange={handleAddressChange}
            searchFunction={searchAddress}
            delay="200"
            localFiltering={false}
            hideArrow
            placeholder="Lieu ; exemple : 1 rue de l’Espoir 33000 Bordeaux"
            errorMessages={addressSelectErrorMessages}
            {itemContent}
          />
          <div
            class="right-s12 top-s12 h-s24 w-s24 text-gray-dark absolute z-10"
          >
            {#if addressFieldValue}
              <button
                type="button"
                class="h-s24 w-s24 inline-block"
                onclick={() => {
                  handleAddressChange(null);
                }}
              >
                <span class="h-s24 w-s24 text-gray-text-alt fill-current">
                  <DeleteBack2FillSystem />
                </span>
                <span class="sr-only">Supprimer le lieu sélectionné</span>
              </button>
            {/if}
          </div>
        </div>
      </div>

      <div
        class="border-gray-02 p-s16 text-f14 flex border-b lg:border-r lg:border-b-0"
      >
        <div
          class="mr-s8 h-s24 w-s24 text-magenta-cta self-center fill-current"
        >
          <SearchLineSystem />
        </div>

        <label for="search-query" class="sr-only"
          >Mots-clés de la recherche</label
        >
        <input
          bind:value={searchQuery}
          id="search-query"
          class="w-full p-s16 rounded-lg"
          maxlength={MAX_QUERY_LENGTH}
          placeholder="Type de structure, thématique, public, mot-clé…"
        />
      </div>

      <div class="flex items-center justify-around p-s12 lg:p-s16">
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
  .grid :global(.autocomplete) {
    @apply block;
  }
  .grid :global(.input-container input) {
    @apply bg-transparent;
  }
  .grid :global(input::placeholder) {
    @apply text-gray-text;
  }
</style>
