<script module lang="ts">
  export const ADDRESS_QUERY_PARAMS = new Set([
    "code_commune",
    "code_departement",
    "code_region",
    "lon",
    "lat",
  ]);
</script>

<script lang="ts">
  import insane from "insane";
  import { onMount } from "svelte";

  import DeleteBack2FillSystem from "svelte-remix/DeleteBack2FillSystem.svelte";
  import MapPin2LineMap from "svelte-remix/MapPin2LineMap.svelte";
  import SearchLineSystem from "svelte-remix/SearchLineSystem.svelte";

  import { goto } from "$app/navigation";
  import { page } from "$app/state";

  import Button from "$lib/components/display/button.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import { formatMunicipality, search as searchBAN } from "$lib/requests/ban";
  import {
    LocationType,
    loadLastLocation,
    saveLastLocation,
    type AddressResult,
  } from "$lib/utils/service-search-keyword";
  import type { BANFeature } from "$lib/requests/ban";
  import { searchDepartment, searchRegion } from "$lib/utils/search-area";

  interface SelectOption {
    value: AddressResult;
    label: string;
  }

  const minCharactersToTriggerSearch = 4;

  function loadAddressFromSearchParams(
    params: URLSearchParams
  ): AddressResult | null {
    const label = params.get("label") || "";
    const singleParam = {
      /* eslint-disable camelcase -- query params conservés en snake_case */
      code_commune: LocationType.City,
      code_departement: LocationType.Department,
      code_region: LocationType.Region,
      /* eslint-enable camelcase */
    };
    for (const [key, kind] of Object.entries(singleParam)) {
      if (params.get(key)) {
        return {
          kind,
          label,
          searchParams: new URLSearchParams({ [key]: params.get(key) || "" }),
        };
      }
    }
    if (params.get("lon") && params.get("lat")) {
      return {
        kind: LocationType.Address,
        label,
        searchParams: new URLSearchParams({
          lon: params.get("lon") || "",
          lat: params.get("lat") || "",
        }),
      };
    }
    return null;
  }

  let addressFieldValue = $state(page.url.searchParams.get("label") || "");
  let addressSelected: AddressResult | null = $state(
    loadAddressFromSearchParams(page.url.searchParams)
  );
  let addressSelectErrorMessage = $state("");
  // Conserve la recherche en cours à l'affichage des résultats : on initialise
  // le champ avec le paramètre `q` présent dans l'URL.
  let searchQuery = $state(page.url.searchParams.get("q") ?? "");

  let isLoading = $state(false);
  const submitDisabled = $derived(!addressSelected && !searchQuery);

  async function searchAddress(addressQuery: string) {
    const addresses: SelectOption[] = [];
    const cities: SelectOption[] = [];
    let banData: BANFeature[];
    try {
      addressSelectErrorMessage = "";
      banData = await searchBAN(addressQuery);
    } catch (error: any) {
      if (error instanceof Error) {
        addressSelectErrorMessage = error.message;
      } else {
        addressSelectErrorMessage =
          "Impossible d’effectuer une recherche d’adresse, veuillez réessayer.";
      }
      banData = [];
    }
    for (const feature of banData) {
      if (feature.properties.type === "municipality") {
        const label = formatMunicipality(feature);
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
              lon: lon.toString(),
              lat: lat.toString(),
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
    const department = searchDepartment(addressQuery);
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
    const region = searchRegion(addressQuery);
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

  function handleAddressChange(newAddress: AddressResult | null) {
    if (newAddress) {
      addressFieldValue = newAddress.label;
      addressSelected = newAddress;
      saveLastLocation(newAddress);
    } else {
      addressFieldValue = "";
      addressSelected = null;
      saveLastLocation(null);
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
      params.append("label", addressFieldValue);
    }
    await goto(`/recherche-mots-cles?${params.toString()}`, {
      noScroll: true,
    });

    isLoading = false;
  }

  onMount(() => {
    if (
      [...ADDRESS_QUERY_PARAMS].some((key) => page.url.searchParams.has(key))
    ) {
      return;
    }
    const lastLocation = loadLastLocation();
    if (lastLocation) {
      addressSelected = lastLocation;
      addressFieldValue = lastLocation.label;
    }
  });
</script>

<div
  class="tag bg-blue-information text-f12 py-s4 px-s8 text-gray-text mb-s6 ml-auto w-fit font-bold uppercase"
>
  Nouveau : recherchez les services d’insertion par mots-clés
</div>

<form action="/recherche-mots-cles" onsubmit={handleSearch}>
  {#if addressSelectErrorMessage}
    <!-- L’id correspond au aria-describedby du <Select …/> en cas d’erreur. -->
    <p id="place-error-0" class="f-16 my-s8 text-service-unavailable-dark">
      {addressSelectErrorMessage}
    </p>
  {/if}
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
              {@html // eslint-disable-line svelte/no-at-html-tags
              insane(item.highlighted?.label ?? item.label, {
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
            // Le aria-describedby est généré par le Select, le DOM de ce
            // composant contient un élément id="place-error-0" pour
            // correspondre.
            errorMessages={addressSelectErrorMessage
              ? ["one element array, to set aria-described-by='place-error-0'"]
              : undefined}
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
          class="p-s16 w-full rounded-lg"
          placeholder="Mots-clés, nom de structure ou de solution, thématiques…"
        />
      </div>

      <div class="p-s12 lg:p-s16 flex items-center justify-around">
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
