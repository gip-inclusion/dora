<script>
  import { goto } from "$app/navigation";

  import Button from "$lib/components/button.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import { searchIcon } from "$lib/icons";
  import { getQuery } from "./_search";

  export let servicesOptions;
  const categoryChoices = servicesOptions.categories;

  let category;
  let subcategory;
  let cityCode;
  let cityLabel;

  let subCategoryChoices = [];

  function handleSearch() {
    const query = getQuery(category, subcategory, cityCode, cityLabel);
    goto(`recherche/?${query}`);
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

<style>
  .wrapper {
    padding: 24px 24px 16px;
    background-color: var(--col-white);
    border-radius: var(--s8);
    box-shadow: var(--shadow-l);
  }

  form {
    display: flex;
    flex-direction: row;
    gap: var(--s16);
  }

  p {
    width: 76%;
    margin: 0 auto;
    color: var(--col-text-alt2);
    font-size: var(--f12);
    text-align: center;
  }
</style>

<div class="wrapper">
  <form on:submit|preventDefault={handleSearch}>
    <Field
      type="select"
      bind:value={category}
      onSelectChange={handleCategoryChange}
      placeholder="Choisissez"
      choices={categoryChoices}
      label="Thématique"
      vertical
      required />

    <Field
      type="select"
      bind:value={subcategory}
      placeholder="Choisissez"
      choices={subCategoryChoices}
      label="Besoin(s)"
      vertical />

    <Field type="custom" label="Lieu" required vertical>
      <CitySearch
        slot="custom-input"
        name="city"
        placeholder="Ville du bénéficiaire"
        handleChange={(city) => {
          console.log(city.properties);
          cityCode = city.properties.citycode;
          cityLabel = `${
            city.properties.label
          } (${city.properties.postcode.slice(0, 2)})`;
        }} />
    </Field>

    <Button
      type="submit"
      label="Trouver"
      icon={searchIcon}
      disabled={!category || !cityCode}
      iconOnLeft
      horizontalBottom
      small />
  </form>
  <p>
    Le service DORA est actuellement <a
      class="underline"
      href="https://beta.gouv.fr/startups/dora.html">en construction</a
    >, et se concentre sur 3 thématiques de services (mobilité, garde d’enfant
    et hébergement/logement) et 3 territoires (Loire-Atlantique, Ardennes et La
    Réunion).
  </p>
</div>
