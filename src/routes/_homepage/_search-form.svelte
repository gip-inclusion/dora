<script>
  import { goto } from "$app/navigation";

  import Button from "$lib/components/button.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import { searchIcon } from "$lib/icons";
  import { getDepartmentFromCityCode } from "$lib/utils";
  import { getQuery } from "./_search";

  export let servicesOptions = {};
  const categoryChoices = servicesOptions.categories;
  categoryChoices?.forEach((choice) => {
    if (["GL", "FL", "CR", "FI", "IL", "DI"].includes(choice.value)) {
      choice.tags = ["nouv."];
    }
  });

  let category;
  let subcategory;
  let cityCode;
  let cityLabel;

  let subCategoryChoices = [];
  const radiusChoices = [
    { value: "10", label: "10 km" },
    { value: "20", label: "20 km" },
    { value: "50", label: "50 km" },
    { value: "100", label: "100 km" },
  ];

  let radius = radiusChoices[0].value;

  function handleSearch() {
    const query = getQuery(category, subcategory, cityCode, radius, cityLabel);
    goto(`recherche?${query}`);
  }

  function handleCategoryChange(cat) {
    subCategoryChoices = cat
      ? servicesOptions.subcategories.filter(({ value }) =>
          value.startsWith(cat)
        )
      : [];
    if (cat && subcategory && !subcategory.startsWith(cat)) subcategory = null;
  }
</script>

<div class="wrapper-top text-center lg:text-left">
  ⚠️ Les premiers départements accessibles à la recherche sont les Ardennes et
  l’Ile de la Réunion.
  <a
    class="underline"
    target="_blank"
    rel="noopener"
    href="https://documentation.dora.fabrique.social.gouv.fr/le-projet-dora/lancement-du-projet-dora/acceleration-de-dora-des-octobre-2021"
  >
    Suivez l’ouverture des autres territoires</a
  >.
</div>

<div class="wrapper">
  {#if categoryChoices}
    <form on:submit|preventDefault={handleSearch}>
      <Field
        type="select"
        name="category"
        bind:value={category}
        onSelectChange={handleCategoryChange}
        placeholder="Choisissez"
        choices={categoryChoices}
        label="Thématique"
        vertical
        required
      />

      <Field
        type="select"
        name="subcategory"
        bind:value={subcategory}
        placeholder="Choisissez"
        choices={subCategoryChoices}
        label="Besoin(s)"
        vertical
        sortSelect
      />

      <Field type="custom" label="Lieu" name="city" required vertical>
        <CitySearch
          slot="custom-input"
          name="city"
          placeholder="Ville du bénéficiaire"
          handleChange={(city) => {
            cityCode = city?.properties.citycode;
            cityLabel = `${city?.properties.label} (${getDepartmentFromCityCode(
              city?.properties.postcode
            )})`;
          }}
        />
      </Field>

      <div class="basis-s112">
        <Field
          type="select"
          name="radius"
          bind:value={radius}
          choices={radiusChoices}
          label="Rayon"
          vertical
          sortSelect
        />
      </div>

      <div class="mb-s16 self-end">
        <Button
          type="submit"
          label="Trouver"
          icon={searchIcon}
          disabled={!category || !cityCode}
          iconOnLeft
          small
          preventDefaultOnMouseDown
        />
      </div>
    </form>
  {:else}
    <p>Impossible de contacter le serveur</p>
  {/if}
</div>

<style lang="postcss">
  .wrapper {
    padding: 24px 24px 16px;
    background-color: var(--col-white);
    border-radius: 0 0 var(--s8) var(--s8);
    box-shadow: var(--shadow-l);
  }

  .wrapper-top {
    padding: 24px 24px 24px;
    background-color: var(--col-magenta-dark);
    border-radius: var(--s8) var(--s8) 0 0;
    box-shadow: var(--shadow-l);
    color: var(--col-white);
  }

  form {
    display: flex;
    flex-direction: column;
    gap: var(--s16);
  }

  @screen lg {
    form {
      flex-direction: row;
    }
  }
</style>
