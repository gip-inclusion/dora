<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import FieldWrapper from "$lib/components/inputs/obsolete/field-wrapper.svelte";
  import SelectField from "$lib/components/inputs/obsolete/select-field.svelte";
  import CitySearch from "$lib/components/inputs/geo/city-search.svelte";

  import {
    arrowDownSIcon,
    deleteBackIcon,
    mapPinIcon,
    searchIcon,
  } from "$lib/icons";
  import type { FeeCondition, ServiceKind, ServicesOptions } from "$lib/types";
  import {
    injectOptGroupAllOptionsInSubCategories,
    injectOptGroupInSubCategories,
  } from "$lib/utils/choice";
  import {
    getDepartmentFromCityCode,
    isInDeploymentDepartments,
  } from "$lib/utils/misc";
  import {
    associateIconToCategory,
    sortByCategories,
    sortCategory,
  } from "$lib/utils/service";
  import { getQuery } from "$lib/utils/service-search";

  export let servicesOptions: ServicesOptions;
  export let cityCode;
  export let cityLabel;
  export let subCategoryIds: string[] = [];
  export let showDeploymentWarning = true;
  export let useAdditionalFilters = false;
  export let kindIds: ServiceKind[] = [];
  export let feeConditions: FeeCondition[] = [];

  let innerWidth;
  const MOBILE_BREAKPOINT = 768; // 'md' from https://tailwindcss.com/docs/screens
  let cityChoiceList;

  function handleSearch() {
    const categoryIds = subCategoryIds
      .filter((value) => value.endsWith("--all"))
      .map((value) => value.replace("--all", ""));

    // Remove sub-categories ending with --all
    const finalSubCategoryIds = subCategoryIds.filter(
      (value) => !value.endsWith("--all")
    );

    const query = getQuery({
      categoryIds,
      subCategoryIds: finalSubCategoryIds,
      cityCode,
      cityLabel,
      kindIds,
      feeConditions,
    });
    goto(`recherche?${query}`);
  }

  function handleSearchIfNotDisabled() {
    if (cityCode && subCategoryIds.length) {
      handleSearch();
    }
  }

  const categories = servicesOptions.categories
    ? associateIconToCategory(sortCategory(servicesOptions.categories))
    : [];

  const subCategories = servicesOptions.categories
    ? sortByCategories(
        servicesOptions.categories,
        injectOptGroupAllOptionsInSubCategories(
          categories,
          injectOptGroupInSubCategories(servicesOptions?.subcategories),
          "Tous les besoins"
        )
      )
    : [];
</script>

<svelte:window bind:innerWidth />

<div class="w-full rounded-md border border-gray-02 bg-white">
  {#if servicesOptions.categories}
    <form class="grid" on:submit|preventDefault={handleSearch}>
      <div
        class="city flex items-center border-b border-gray-02 p-s16 text-f14 lg:border-r lg:border-b-0"
        class:has-value={!!cityCode}
      >
        <div class="mr-s8 h-s24 w-s24 fill-current text-magenta-cta">
          {@html mapPinIcon}
        </div>

        <FieldWrapper label="Lieu" name="city" required hideLabel>
          <div
            class="absolute top-s12 right-s12 z-10 h-s24 w-s24 text-gray-dark"
          >
            {#if cityCode}
              <button
                class="inline-block h-s24 w-s24"
                on:click={() => {
                  cityCode = "";
                  cityLabel = "";
                  cityChoiceList = {};
                }}
              >
                <span class="h-s24 w-s24 fill-current text-gray-text-alt">
                  {@html deleteBackIcon}
                </span>
              </button>
            {:else}
              <span class="h-s24 w-s24 fill-current">
                {@html arrowDownSIcon}
              </span>
            {/if}
          </div>

          <CitySearch
            id="city"
            initialValue={cityLabel}
            bind:value={cityChoiceList}
            placeholder="Rechercher par lieu : ville"
            onChange={(city) => {
              cityCode = city?.code;
              cityLabel = `${city?.name} (${getDepartmentFromCityCode(
                city?.code
              )})`;
            }}
          />
        </FieldWrapper>
      </div>

      <div
        class="flex justify-between border-b border-gray-02 p-s16 text-f14 lg:border-r lg:border-b-0"
      >
        <div
          class="mr-s8 h-s24 w-s24 self-center fill-current text-magenta-cta"
        >
          {@html searchIcon}
        </div>

        <SelectField
          inputMode={innerWidth < MOBILE_BREAKPOINT ? "none" : undefined}
          hideLabel
          isMultiple
          withAutoComplete
          withClearButton
          style="search"
          label="Besoins"
          name="subcategories"
          placeholder="Recherche par besoins"
          bind:value={subCategoryIds}
          choices={subCategories}
          optGroups={categories}
        />
      </div>

      <div class="p-s12 text-center lg:p-s16">
        <Button
          extraClass="h-s48"
          type="submit"
          label="Rechercher"
          disabled={!cityCode}
          preventDefaultOnMouseDown
        />
      </div>
    </form>

    {#if showDeploymentWarning && cityCode && !isInDeploymentDepartments(cityCode, servicesOptions)}
      <div
        class=" rounded-b-md border-t border-gray-02 bg-blue-light p-s16 text-center text-france-blue"
      >
        <span>
          Sur votre territoire, le référencement des services débute – il se
          peut que votre recherche aboutisse à peu de résultats.
        </span>
      </div>
    {/if}
  {:else}
    <p class="p-s16 text-center">Impossible de contacter le serveur</p>
  {/if}
  {#if useAdditionalFilters}
    <div
      class="flex flex-col rounded-b-md border-t border-gray-02 bg-white p-s16 text-f14 md:flex-row"
    >
      <div class="mr-s12 mb-s12 md:mb-s0">
        <SelectField
          hideLabel
          isMultiple
          style="filter"
          label="Type de service"
          minDropdownWidth="min-w-[200px]"
          name="subcategories"
          placeholder="Type de service"
          bind:value={kindIds}
          choices={servicesOptions.kinds}
          onChange={handleSearchIfNotDisabled}
        />
      </div>
      <div>
        <SelectField
          hideLabel
          isMultiple
          minDropdownWidth="min-w-[240px]"
          style="filter"
          label="Frais à charge"
          name="fee"
          placeholder="Frais à charge"
          bind:value={feeConditions}
          choices={servicesOptions.feeConditions}
          onChange={handleSearchIfNotDisabled}
        />
      </div>
    </div>
  {/if}
</div>

<style lang="postcss">
  .grid {
    grid-template-columns: 1fr;
    display: grid;
  }
  ::global(#subcategories) {
    position: relative;
  }
  @screen lg {
    ::global(#subcategories) {
      position: absolute;
    }
    .grid {
      grid-template-columns: 3fr 3fr 1fr;
    }
  }

  .grid :global(.autocomplete-input) {
    @apply border-0;
  }
  .grid :global(.city) {
    @apply text-magenta-dark;
  }
  .grid :global(.input-container input) {
    @apply bg-transparent;
  }
  .grid :global(input::placeholder) {
    @apply text-gray-text;
  }
</style>
