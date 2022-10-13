<script>
  import { goto } from "$app/navigation";

  import Button from "$lib/components/button.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import { searchIcon } from "$lib/icons";
  import { getDepartmentFromCityCode, moveToTheEnd } from "$lib/utils";
  import { getQuery } from "./_search";

  export let servicesOptions = {};

  let categoryId;
  let subCategoryId;
  let cityCode;
  let cityLabel;

  let subCategoryChoices = [];

  function handleSearch() {
    const query = getQuery({ categoryId, subCategoryId, cityCode, cityLabel });
    goto(`recherche?${query}`);
  }

  function handleCategoryChange(category) {
    subCategoryChoices = category
      ? servicesOptions.subcategories.filter(({ value }) =>
          value.startsWith(category)
        )
      : [];

    subCategoryChoices = moveToTheEnd(subCategoryChoices, "label", "Autre", {
      sortBeginning: true,
    });

    if (category && subCategoryId && !subCategoryId.startsWith(category))
      subCategoryId = null;
  }
</script>

<div id="home-search-form" class="rounded-md p-s24 shadow-md">
  {#if servicesOptions.categories}
    <form
      on:submit|preventDefault={handleSearch}
      class="grid w-full gap-s16 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-11"
    >
      <div class="md:col-span-1 lg:col-span-3">
        <Field
          type="select"
          name="category"
          bind:value={categoryId}
          onSelectChange={handleCategoryChange}
          placeholder="Sélectionner"
          choices={servicesOptions.categories}
          label="Thématique"
          vertical
          required
          sortSelect
        />
      </div>

      <div class="md:col-span-1 lg:col-span-3">
        <Field
          type="select"
          name="subcategory"
          bind:value={subCategoryId}
          placeholder="Sélectionner"
          choices={subCategoryChoices}
          label="Besoin"
          vertical
        />
      </div>
      <div class="md:col-span-2 lg:col-span-3">
        <Field type="custom" label="Lieu" name="city" required vertical>
          <CitySearch
            slot="custom-input"
            name="city"
            placeholder="Ville du bénéficiaire"
            onChange={(city) => {
              cityCode = city?.code;
              cityLabel = `${city?.name} (${getDepartmentFromCityCode(
                city?.code
              )})`;
            }}
          />
        </Field>
      </div>

      <div class="self-end md:col-span-2 lg:col-span-2">
        <Button
          extraClass="h-s48"
          type="submit"
          label="Rechercher"
          icon={searchIcon}
          disabled={!categoryId || !cityCode}
          small
          wFull
          preventDefaultOnMouseDown
        />
      </div>
    </form>
  {:else}
    <p>Impossible de contacter le serveur</p>
  {/if}
</div>
