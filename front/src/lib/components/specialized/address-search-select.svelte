<script lang="ts">
  import insane from "insane";
  import {
    type LocationOption,
    LocationType,
    parseLocation,
    serializeLocation,
  } from "$lib/utils/service-search-keyword";
  import Select from "$lib/components/inputs/select/select.svelte";
  import {
    getRegionDepartments,
    searchDepartment,
    searchRegion,
  } from "$lib/utils/search-area";
  import {
    type EpcisAndCitiesResults,
    searchEpcisAndCities,
  } from "$lib/requests/geo";

  interface Props {
    id: string;
    addressSelectErrorMessage: string;
    addressFieldValue: string;
    handleAddressChange: (newLocations: string[] | null) => void;
    placeholder: string;
    multiple?: boolean;
    value?: string[];
    initialLabels?: LocationOption[];
    extraClass?: string;
  }

  let {
    id,
    addressSelectErrorMessage = $bindable(),
    addressFieldValue = $bindable(),
    handleAddressChange,
    placeholder,
    multiple,
    value = $bindable([]),
    initialLabels = [],
    extraClass = "",
  }: Props = $props();

  const MIN_CHARACTERS_TO_TRIGGER_SEARCH = 3;
  const SEARCH_ERROR_MESSAGE =
    "Impossible d’effectuer une recherche d’adresse, veuillez réessayer.";

  async function searchAddress(addressQuery: string) {
    addressSelectErrorMessage = "";
    const locations: LocationOption[] = [];

    let searchResults: EpcisAndCitiesResults | null = null;
    try {
      searchResults = await searchEpcisAndCities(addressQuery);
    } catch (error) {
      addressSelectErrorMessage =
        error instanceof Error ? error.message : SEARCH_ERROR_MESSAGE;
    }

    if (searchResults) {
      locations.push(
        ...searchResults.cities.map((city) => ({
          label: `${city.label} (${city.value})`,
          value: serializeLocation({
            type: LocationType.City,
            codes: [city.value],
          }),
        })),
        ...searchResults.epcis.map((epci) => ({
          label: epci.label,
          value: serializeLocation({
            type: LocationType.EPCI,
            codes: [epci.value],
          }),
        }))
      );
    } else if (!addressSelectErrorMessage) {
      addressSelectErrorMessage = SEARCH_ERROR_MESSAGE;
    }

    // les départements et régions sont résolus localement : ils restent
    // disponibles même si la recherche distante a échoué
    const department = searchDepartment(addressQuery);
    if (department) {
      locations.unshift({
        label: `${department.label} (${department.code})`,
        value: serializeLocation({
          type: LocationType.Department,
          codes: [department.code],
        }),
      });
    }
    const region = searchRegion(addressQuery);
    if (region) {
      locations.unshift({
        label: region.label,
        value: serializeLocation({
          type: LocationType.Region,
          codes: getRegionDepartments(region.code),
        }),
      });
    }
    return locations;
  }
</script>

<div class="relative w-full">
  <label class="sr-only" for="place">
    Lieu (tapez au moins {MIN_CHARACTERS_TO_TRIGGER_SEARCH} caractères pour rechercher)
  </label>
  {#snippet itemContent({ item })}
    {@const { type } = parseLocation(item.value)}
    <span>
      {@html // eslint-disable-line svelte/no-at-html-tags
      insane(item.highlighted?.label ?? item.label, {
        allowedTags: ["b"],
      })}
      <span class="text-gray-text-alt2">
        {#if type === LocationType.City}
          · Commune
        {:else if type === LocationType.Department}
          · Département
        {:else if type === LocationType.Region}
          · Région
        {:else if type === LocationType.EPCI}
          · Intercommunalité
        {/if}
      </span>
    </span>
  {/snippet}
  <Select
    {id}
    {multiple}
    {initialLabels}
    minCharactersToSearch={MIN_CHARACTERS_TO_TRIGGER_SEARCH}
    bind:searchText={addressFieldValue}
    bind:value
    onChange={handleAddressChange}
    searchFunction={searchAddress}
    delay="200"
    localFiltering={false}
    hideArrow
    {placeholder}
    errorMessages={addressSelectErrorMessage
      ? ["one element array, to set aria-described-by='place-error-0'"]
      : undefined}
    {itemContent}
    {extraClass}
  />
</div>
