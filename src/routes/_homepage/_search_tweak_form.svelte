<script>
  import { goto } from "$app/navigation";

  import Button from "$lib/components/button.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import { getQuery } from "./_search";

  export let servicesOptions;
  export let numResults;
  export let category;
  export let subcategory;
  export let cityCode;

  function handleSearch() {
    const query = getQuery(category, subcategory, cityCode);
    goto(`recherche/?${query}`);
  }

  $: catChoices = servicesOptions.categories;

  $: subCatChoices = servicesOptions.subcategories.filter(({ value }) =>
    value.startsWith(category)
  );

  function handleCategoryChange(cat) {
    subCatChoices = cat
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
    box-shadow: var(--shadow-md);
  }

  h3 {
    color: var(--col-france-blue);
  }

  form {
    display: flex;
    flex-direction: column;
    gap: var(--s16);
  }

  p {
    margin-top: var(--s16);
    color: var(--col-text-alt2);
    font-size: var(--f12);
    text-align: center;
  }
</style>

<div class="wrapper">
  <h3>Affinez votre recherche</h3>

  {#if numResults}
    <div class="text-gray-text-alt2 text-sm mt-2">
      {numResults} résultat{#if numResults > 1}s{/if}
    </div>
  {/if}
  <div class="border-t border-gray-01 my-3/2" />
  <form on:submit|preventDefault={handleSearch}>
    <Field
      type="select"
      bind:value={category}
      onSelectChange={handleCategoryChange}
      placeholder="Choisissez"
      choices={catChoices}
      label="Thématique"
      vertical
      required />

    <Field
      type="select"
      bind:value={subcategory}
      placeholder="Choisissez"
      choices={subCatChoices}
      label="Besoin(s)"
      vertical />

    <Field type="custom" label="Lieu" required vertical>
      <CitySearch
        slot="custom-input"
        name="city"
        placeholder="Ville du bénéficiaire"
        handleChange={(city) => (cityCode = city.properties.citycode)} />
    </Field>

    <Button
      type="submit"
      label="Mettre à jour"
      disabled={!category || !cityCode} />
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
