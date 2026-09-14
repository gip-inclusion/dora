<script lang="ts">
  import insane from "insane";

  import FieldGroup from "$lib/components/display/field-group.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import {
    LOCATION_TYPE_BY_NAME,
    type LocationOption,
    LocationType,
    parseLocation,
    serializeLocation,
  } from "$lib/utils/service-search-keyword";

  import {
    getRegionDepartments,
    searchDepartment,
    searchRegion,
  } from "$lib/utils/search-area";
  import {
    type EpcisAndCitiesResults,
    searchEpcisAndCities,
  } from "$lib/requests/geo";
  import type { FieldGroupProps } from "$lib/components/specialized/services/types";

  let { service = $bindable() }: Omit<FieldGroupProps, "model"> = $props();

  const MIN_CHARACTERS_TO_TRIGGER_SEARCH = 3;

  let addressFieldValue = $state("");
  let addressSelectErrorMessage = $state("");

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

  // les territoires déjà enregistrés ne figurent dans aucun résultat de
  // recherche : le back nous en fournit les libellés, reconstitués à partir des
  // seuls codes stockés
  const initialChoices = (service.zoneEligibiliteDisplay ?? []).map(
    ({ label, type, codes }) => ({
      label,
      value: serializeLocation({ type: LOCATION_TYPE_BY_NAME[type], codes }),
    })
  );

  let selectedValues = $state(initialChoices.map((choice) => choice.value));

  // en sélection multiple, le Select transmet la totalité des valeurs
  // sélectionnées, et non la dernière ajoutée
  function handleAddressChange(newLocations: string[] | null) {
    if (newLocations?.length) {
      service.zoneEligibilite = [
        ...new Set(
          newLocations.flatMap((location) => parseLocation(location).codes)
        ),
      ];
    } else {
      addressFieldValue = "";
    }
  }
</script>

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

<FieldGroup title="Périmètre d'éligibilité" showSeparator={false}>
  <FieldModel>
    <FieldWrapper
      id="zoneEligibilite"
      label="Secteurs éligibles"
      descriptionText="Par défaut au national. Précisez le ou les territoires concernés : départements, communes,…"
    >
      <div class="relative w-full">
        <Select
          id="zoneEligibilite"
          multiple
          bind:searchText={addressFieldValue}
          bind:value={selectedValues}
          onChange={handleAddressChange}
          searchFunction={searchAddress}
          initialLabels={initialChoices}
          minCharactersToSearch={MIN_CHARACTERS_TO_TRIGGER_SEARCH}
          delay="200"
          localFiltering={false}
          hideArrow
          placeholder="Saisissez un département, une commune…"
          errorMessages={addressSelectErrorMessage
            ? ["zoneEligibilite-error-0"]
            : undefined}
          {itemContent}
          extraClass="w-full"
        />
        {#if addressSelectErrorMessage}
          <!-- L’id correspond au aria-describedby du <Select …/> en cas d’erreur. -->
          <p
            id="zoneEligibilite-error-0"
            class="f-16 my-s8 text-service-unavailable-dark"
          >
            {addressSelectErrorMessage}
          </p>
        {/if}
      </div>
    </FieldWrapper>
  </FieldModel>
</FieldGroup>
