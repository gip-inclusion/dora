<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import SelectField from "$lib/components/inputs/obsolete/select-field.svelte";
  import CitySearch from "$lib/components/inputs/geo/city-search.svelte";

  import {
    arrowDownSIcon,
    deleteBackIcon,
    listCheckIcon,
    mapPinIcon,
    searchIcon,
  } from "$lib/icons";
  import type {
    Choice,
    FeeCondition,
    ServiceKind,
    ServicesOptions,
  } from "$lib/types";
  import {
    getDepartmentFromCityCode,
    isInDeploymentDepartments,
  } from "$lib/utils/misc";
  import {
    associateIconToCategory,
    sortCategory,
    sortSubcategory,
  } from "$lib/utils/service";
  import { getQueryString } from "$lib/utils/service-search";
  import { onMount } from "svelte";
  import { refreshUserInfo, userInfo } from "$lib/utils/auth";
  import {
    isCurrentSearchInUserSavedSearchs,
    saveSearch,
  } from "$lib/requests/saved-search";

  export let servicesOptions: ServicesOptions;
  export let cityCode;
  export let cityLabel;
  export let categoryId: string | undefined = undefined;
  export let subCategoryIds: string[] = [];
  export let showDeploymentWarning = true;
  export let useAdditionalFilters = false;
  export let kindIds: ServiceKind[] = [];
  export let feeConditions: FeeCondition[] = [];

  let innerWidth;
  let requestingSave = false;
  let refreshDisabled = true;
  const MOBILE_BREAKPOINT = 768; // 'md' from https://tailwindcss.com/docs/screens
  let cityChoiceList;
  let subCategories: Choice[] = [];

  $: query = getQueryString({
    categoryIds: [categoryId ? categoryId : ""],
    subCategoryIds: subCategoryIds.filter((value) => !value.endsWith("--all")),
    cityCode,
    cityLabel,
    kindIds,
    feeConditions,
  });

  const categories = servicesOptions.categories
    ? associateIconToCategory(sortCategory(servicesOptions.categories))
    : [];

  function handleSearch() {
    refreshDisabled = true;
    goto(`recherche?${query}`, { noScroll: true });
  }

  async function doSaveSearch() {
    requestingSave = true;
    await saveSearch({
      category: categoryId,
      subcategories: subCategoryIds.filter((value) => !value.endsWith("--all")),
      cityCode,
      cityLabel,
      kinds: kindIds,
      fees: feeConditions,
    });
    await refreshUserInfo();
    requestingSave = false;
  }

  function enableRefreshButton() {
    refreshDisabled = false;
  }

  function handleCategoryChange(clearSubCategories = false) {
    enableRefreshButton();

    if (clearSubCategories) {
      subCategoryIds = [];
    }
    if (categoryId) {
      subCategories = sortSubcategory([
        {
          value: `${categoryId}--all`,
          label: "Tous les besoins",
        },
        ...servicesOptions.subcategories.filter((sub) =>
          sub.value.startsWith(categoryId)
        ),
      ]);
    } else {
      subCategories = [];
    }
  }

  onMount(() => {
    handleCategoryChange();
  });
</script>

<svelte:window bind:innerWidth />

<form on:submit|preventDefault={handleSearch}>
  <div class="w-full rounded-md border border-gray-02 bg-white">
    {#if servicesOptions.categories}
      <div class="grid" class:with-subcategories={useAdditionalFilters}>
        <div
          class="city flex items-center border-b border-gray-02 p-s16 text-f14 lg:border-b-0 lg:border-r"
          class:has-value={!!cityCode}
        >
          <div class="mr-s8 h-s24 w-s24 fill-current text-magenta-cta">
            {@html mapPinIcon}
          </div>
          <div class="relative w-full">
            <label class="sr-only" for="city">
              Lieu
              <span class="text-error">*</span>
            </label>

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

                enableRefreshButton();
              }}
            />

            <div
              class="absolute right-s12 top-s12 z-10 h-s24 w-s24 text-gray-dark"
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
                  <span class="sr-only">Supprimer la ville sélectionnée</span>
                </button>
              {:else}
                <span class="h-s24 w-s24 fill-current">
                  {@html arrowDownSIcon}
                </span>
              {/if}
            </div>
          </div>
        </div>

        <div
          class="subcategories-search flex border-b border-gray-02 px-s16 py-s24 text-f14 lg:border-b-0 lg:border-r lg:py-s16"
        >
          <div
            class="mr-s8 h-s24 w-s24 self-center fill-current text-magenta-cta"
          >
            {@html searchIcon}
          </div>

          <SelectField
            inputMode={innerWidth < MOBILE_BREAKPOINT ? "none" : undefined}
            hideLabel
            withClearButton
            style="search"
            label="Thématiques"
            name="categories"
            placeholder="Recherche par thématiques"
            bind:value={categoryId}
            choices={categories}
            onChange={() => handleCategoryChange(true)}
          />
        </div>

        {#if useAdditionalFilters}
          <div
            class="subcategories-search flex border-b border-gray-02 px-s16 py-s24 text-f14 lg:border-b-0 lg:border-r lg:py-s16"
          >
            <div
              class="mr-s8 h-s24 w-s24 self-center fill-current text-magenta-cta"
            >
              {@html listCheckIcon}
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
        {:else}
          <div class="p-s12 text-center lg:p-s16">
            <Button
              extraClass="h-s48"
              type="submit"
              label="Rechercher"
              disabled={!cityCode}
              preventDefaultOnMouseDown
            />
          </div>
        {/if}
      </div>

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
        <div class="mb-s12 mr-s12 md:mb-s0">
          <SelectField
            hideLabel
            isMultiple
            style="filter"
            label="Type de service"
            minDropdownWidth="min-w-[200px]"
            name="kinds"
            placeholder="Type de service"
            bind:value={kindIds}
            choices={servicesOptions.kinds}
            onChange={enableRefreshButton}
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
            onChange={enableRefreshButton}
          />
        </div>
      </div>
    {/if}
  </div>

  {#if useAdditionalFilters}
    <div class="mt-s24 flex justify-center gap-s16 lg:p-s16">
      <Button
        extraClass="h-s48"
        type="submit"
        label="Actualiser la recherche"
        disabled={!cityCode || refreshDisabled}
        on:click={handleSearch}
        preventDefaultOnMouseDown
      />

      {#if isCurrentSearchInUserSavedSearchs($userInfo, query)}
        <Button
          extraClass="h-s48"
          secondary
          label="Alerte déjà créée"
          disabled
          on:click={doSaveSearch}
          preventDefaultOnMouseDown
        />
      {:else}
        <Button
          extraClass="h-s48"
          secondary
          label="Créer une alerte"
          disabled={!cityCode || requestingSave}
          on:click={doSaveSearch}
          preventDefaultOnMouseDown
        />
      {/if}
    </div>
  {/if}
</form>

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
    .with-subcategories {
      grid-template-columns: 1fr 1fr 1fr;
    }
  }

  .subcategories-search :global(.field-wrapper) {
    @apply relative w-[100%];
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
