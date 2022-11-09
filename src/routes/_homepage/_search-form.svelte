<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/button.svelte";

  import FieldWrapper from "$lib/components/form/field-wrapper.svelte";
  import SelectField from "$lib/components/form/select/select-field.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import {
    arrowDownSIcon,
    deleteBackIcon,
    informationIcon,
    mapPinIcon,
    searchIcon,
  } from "$lib/icons";
  import type { FeeCondition, ServicesOptions } from "$lib/types";
  import { getDepartmentFromCityCode } from "$lib/utils";
  import {
    injectOptGroupAllOptionsInSubCategories,
    injectOptGroupInSubCategories,
  } from "$lib/utils/choice";
  import { isInDeploymentDepartments } from "$lib/utils/city";
  import {
    associateIconToCategory,
    sortByCategories,
    sortCategory,
  } from "$lib/utils/service";
  import { getQuery } from "./_search";

  export let servicesOptions: ServicesOptions;
  export let cityCode;
  export let cityLabel;
  export let subCategoryIds: string[] = [];
  export let showDeploymentWarning = true;
  export let useAdditionalFilters = false;
  export let kindId: string | undefined = undefined;
  export let fee: FeeCondition[] = [];

  let cityChoiceList;

  function handleSearch() {
    const categoryIds = subCategoryIds
      .filter((v) => v.endsWith("--all"))
      .map((v) => v.replace("--all", ""));

    // Remove sub-categories ending with --all
    const finalSubCategoryIds = subCategoryIds.filter(
      (v) => !v.endsWith("--all")
    );

    const query = getQuery({
      categoryIds,
      subCategoryIds: finalSubCategoryIds,
      cityCode,
      cityLabel,
      fee,
      kindId,
    });
    goto(`recherche?${query}`);
  }

  const categories = associateIconToCategory(
    sortCategory(servicesOptions.categories)
  );

  const subCategories = sortByCategories(
    servicesOptions.categories,
    injectOptGroupAllOptionsInSubCategories(
      categories,
      injectOptGroupInSubCategories(servicesOptions.subcategories),
      "Tous les besoins"
    )
  );
</script>

<div class="w-full rounded border border-gray-02 bg-white">
  {#if servicesOptions.categories}
    <form class="grid" on:submit|preventDefault={handleSearch}>
      <div
        class="city flex items-center border-b border-gray-02 p-s24 text-f14 lg:border-r lg:border-b-0"
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
            name="city"
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
        class="flex justify-between border-b border-gray-02 p-s24 text-f14 lg:border-r lg:border-b-0"
      >
        <div
          class="mr-s8 h-s24 w-s24 self-center fill-current text-magenta-cta"
        >
          {@html searchIcon}
        </div>

        <SelectField
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

      <div class="p-s12 text-center lg:p-s24">
        <Button
          extraClass="h-s48"
          type="submit"
          label="Rechercher"
          disabled={subCategoryIds.length === 0 || !cityCode}
          preventDefaultOnMouseDown
        />
      </div>
    </form>
  {:else}
    <p>Impossible de contacter le serveur</p>
  {/if}

  {#if showDeploymentWarning && cityCode && !isInDeploymentDepartments(cityCode, servicesOptions)}
    <div
      class="flex border-t border-gray-02 bg-blue-light p-s24 font-bold text-france-blue"
    >
      <span class="mr-s16 h-s24 w-s24 fill-current">
        {@html informationIcon}
      </span>
      <span>
        La plateforme DORA n’est pas encore déployée sur votre territoire, il se
        peut que votre recherche aboutisse à peu de résultats.
      </span>
    </div>
  {/if}

  {#if useAdditionalFilters}
    <div
      class="flex flex-col border-t border-gray-02 bg-white p-s24 text-f14 md:flex-row"
    >
      <div class="mr-s12 mb-s12 md:mb-s0">
        <SelectField
          hideLabel
          style="filter"
          label="Type de service"
          minDropdownWidth="min-w-[200px]"
          name="subcategories"
          placeholder="Type de service"
          bind:value={kindId}
          choices={servicesOptions.kinds}
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
          bind:value={fee}
          choices={servicesOptions.feeConditions}
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
