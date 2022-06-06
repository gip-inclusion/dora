<script>
  import { goto } from "$app/navigation";

  import Button from "$lib/components/button.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import { searchIcon } from "$lib/icons";
  import { getDepartmentFromCityCode } from "$lib/utils";
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

  function handleCategoryChange(cat) {
    subCategoryChoices = cat
      ? servicesOptions.subcategories.filter(({ value }) =>
          value.startsWith(cat)
        )
      : [];
    if (cat && subCategoryId && !subCategoryId.startsWith(cat))
      subCategoryId = null;
  }
</script>

<div class="rounded-md bg-white p-s24 shadow-l">
  {#if servicesOptions.categories}
    <form
      on:submit|preventDefault={handleSearch}
      class="flex flex-col gap-s16 lg:flex-row"
    >
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

      <Field
        type="select"
        name="subcategory"
        bind:value={subCategoryId}
        placeholder="Sélectionner"
        choices={subCategoryChoices}
        label="Besoin"
        vertical
        sortSelect
      />

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

      <div class="flex-1 lg:self-end">
        <Button
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
