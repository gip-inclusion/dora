<script lang="ts">
  import { onMount } from "svelte";

  import DeleteBack2FillSystem from "svelte-remix/DeleteBack2FillSystem.svelte";
  import ListCheck2Editor from "svelte-remix/ListCheck2Editor.svelte";
  import MapPin2LineMap from "svelte-remix/MapPin2LineMap.svelte";
  import SearchLineSystem from "svelte-remix/SearchLineSystem.svelte";

  import { goto } from "$app/navigation";

  import Button from "$lib/components/display/button.svelte";
  import SelectField from "$lib/components/inputs/obsolete/select-field.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import type {
    Choice,
    FeeCondition,
    FundingLabel,
    LocationKind,
    ServiceKind,
    ServicesOptions,
  } from "$lib/types";
  import { getDepartmentFromCityCode } from "$lib/utils/misc";
  import {
    associateIconToCategory,
    sortCategory,
    sortSubcategory,
  } from "$lib/utils/service";
  import { getQueryString } from "$lib/utils/service-search";

  interface Props {
    servicesOptions: ServicesOptions;
    cityCode?: string;
    cityLabel?: string;
    label?: string;
    lon?: number;
    lat?: number;
    categoryId?: string;
    subCategoryIds?: string[];
    useAdditionalFilters?: boolean;
    kindIds?: ServiceKind[];
    feeConditions?: FeeCondition[];
    locationKinds?: LocationKind[];
    fundingLabels?: Array<FundingLabel["value"]>;
    initialSearch?: boolean;
  }

  let {
    servicesOptions,
    cityCode = $bindable(),
    cityLabel = $bindable(),
    label = $bindable(""),
    lon = $bindable(),
    lat = $bindable(),
    categoryId = $bindable(),
    subCategoryIds = $bindable([]),
    useAdditionalFilters = false,
    kindIds = [],
    feeConditions = [],
    locationKinds = [],
    fundingLabels = [],
    initialSearch = false,
  }: Props = $props();

  let innerWidth = $state();
  let submitDisabled = $state(!initialSearch);
  let refreshMode = $state(false);
  const MOBILE_BREAKPOINT = 768; // 'md' from https://tailwindcss.com/docs/screens
  let subCategories: Choice[] = $state([]);

  let query = $derived(
    getQueryString({
      categoryIds: [categoryId ? categoryId : ""],
      subCategoryIds: subCategoryIds.filter(
        (value) => !value.endsWith("--all")
      ),
      cityCode,
      cityLabel,
      label,
      kindIds,
      feeConditions,
      locationKinds,
      fundingLabels,
      lon,
      lat,
    })
  );

  const categories = servicesOptions?.categories
    ? associateIconToCategory(sortCategory(servicesOptions.categories))
    : [];

  function getCityLabel(address) {
    return `${address.properties.city} (${getDepartmentFromCityCode(
      address.properties.citycode
    )})`;
  }

  function getAddressLabel(address) {
    return address.properties.type === "municipality"
      ? getCityLabel(address)
      : address.properties.label;
  }

  const banAPIUrl = "https://api-adresse.data.gouv.fr/search/";

  async function searchAddress(addrQuery) {
    const url = `${banAPIUrl}?q=${encodeURIComponent(addrQuery)}&limit=10`;
    const response = await fetch(url);
    const jsonResponse = await response.json();
    const results = jsonResponse.features.map((feature) => ({
      value: feature,
      label: getAddressLabel(feature),
    }));
    return results;
  }

  function enableRefreshButton() {
    if (!initialSearch) {
      refreshMode = true;
      submitDisabled = false;
    }
  }

  function handleAddressChange(address) {
    if (address) {
      const props = address.properties;
      cityCode = props.citycode;
      cityLabel = getCityLabel(address);
      label = getAddressLabel(address);
      [lon, lat] =
        address.properties.type === "municipality"
          ? [undefined, undefined]
          : address.geometry.coordinates;
      enableRefreshButton();
    } else {
      cityCode = cityLabel = lon = lat = undefined;
      label = "";
    }
  }

  function handleSearch(event: Event) {
    event.preventDefault();
    submitDisabled = true;
    refreshMode = false;
    goto(`/recherche?${query}`, { noScroll: true });
  }

  function loadSubCategories() {
    if (categoryId) {
      const allSubCategoriesValue = `${categoryId}--all`;
      subCategories = sortSubcategory([
        {
          value: allSubCategoriesValue,
          label: "Tous les besoins",
        },
        ...servicesOptions.subcategories.filter((sub) =>
          sub.value.startsWith(categoryId)
        ),
      ]);
      subCategoryIds = [allSubCategoriesValue];
    } else {
      subCategories = [];
    }
  }

  function handleCategoryChange() {
    enableRefreshButton();
    subCategoryIds = [];
    loadSubCategories();
  }

  onMount(() => {
    loadSubCategories();
  });
</script>

<svelte:window bind:innerWidth />

<form onsubmit={handleSearch}>
  <div class="border-gray-02 w-full rounded-lg border bg-white">
    {#if servicesOptions.categories}
      <div class="grid" class:with-subcategories={useAdditionalFilters}>
        <div
          class="city border-gray-02 p-s16 text-f14 flex items-center border-b lg:border-r lg:border-b-0"
          class:has-value={!!cityCode}
        >
          <div class="mr-s8 h-s24 w-s24 text-magenta-cta fill-current">
            <MapPin2LineMap />
          </div>
          <div class="relative w-full">
            <label class="sr-only" for="city">
              Lieu
              <span class="text-error">*</span>
            </label>
            <Select
              id="address"
              bind:searchText={label}
              onChange={handleAddressChange}
              hideArrow
              searchFunction={searchAddress}
              delay="200"
              localFiltering={false}
              minCharactersToSearch="3"
              placeholder="Lieu ; exemple : 1 rue de l’Espoir 33000 Bordeaux"
            />
            <div
              class="right-s12 top-s12 h-s24 w-s24 text-gray-dark absolute z-10"
            >
              {#if cityCode}
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
          class="subcategories-search border-gray-02 px-s16 py-s24 text-f14 lg:py-s16 flex border-b lg:border-r lg:border-b-0"
        >
          <div
            class="mr-s8 h-s24 w-s24 text-magenta-cta self-center fill-current"
          >
            <SearchLineSystem />
          </div>

          <SelectField
            inputMode={innerWidth < MOBILE_BREAKPOINT ? "none" : undefined}
            hideLabel
            withClearButton
            style="search"
            label="Thématiques"
            name="categories"
            placeholder="Sélectionnez une thématique"
            bind:value={categoryId}
            choices={categories}
            onChange={handleCategoryChange}
          />
        </div>

        {#if useAdditionalFilters}
          <div
            class="subcategories-search border-gray-02 px-s16 py-s24 text-f14 lg:py-s16 flex border-b lg:border-r lg:border-b-0"
          >
            <div
              class="mr-s8 h-s24 w-s24 text-magenta-cta self-center fill-current"
            >
              <ListCheck2Editor />
            </div>

            {#key subCategories}
              <SelectField
                inputMode={innerWidth < MOBILE_BREAKPOINT ? "none" : undefined}
                hideLabel
                isMultiple
                withClearButton
                style="search"
                label="Besoins"
                name="subcategories"
                placeholder="Recherche par besoins"
                bind:value={subCategoryIds}
                choices={subCategories}
                onChange={enableRefreshButton}
              />
            {/key}
          </div>
        {/if}
        <div class="p-s12 lg:p-s16 text-center">
          <Button
            extraClass="h-s48"
            type="submit"
            label={refreshMode ? "Actualiser" : "Rechercher"}
            title={submitDisabled
              ? "Modifiez un des critères avant d’actualiser la recherche"
              : undefined}
            disabled={!cityCode || submitDisabled}
          />
        </div>
      </div>
    {:else}
      <p class="p-s16 text-center">Impossible de contacter le serveur</p>
    {/if}
  </div>
</form>

<style lang="postcss">
  @reference "../../../app.css";

  .grid {
    grid-template-columns: 1fr;
    display: grid;
  }
  ::global(#subcategories) {
    position: relative;
  }
  @media (width >= 64rem) {
    ::global(#subcategories) {
      position: absolute;
    }
    .grid {
      grid-template-columns: 3fr 3fr 1fr;
    }
    .with-subcategories {
      grid-template-columns: 2fr 2fr 2fr 1fr;
    }
  }

  .subcategories-search :global(.field-wrapper) {
    position: relative;
    width: 100%;
  }
  .subcategories-search :global(.label-container) {
    @apply sr-only;
  }

  .grid :global(.autocomplete-input) {
    @apply border-0;
  }
  .grid :global(.city) {
    @apply text-magenta-dark;
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
