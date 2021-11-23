<script>
  import { goto } from "$app/navigation";

  import Button from "$lib/components/button.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import { getDepartmentFromCityCode } from "$lib/utils";

  import Collapsable from "./_collapsable.svelte";
  import { getQuery } from "./_search";

  export let servicesOptions;
  export let numResults;
  export let category;
  export let subcategory;
  export let cityCode;
  export let cityLabel;

  function handleSearch() {
    const query = getQuery(category, subcategory, cityCode, cityLabel);
    goto(`recherche?${query}`);
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
</style>

<div class="wrapper">
  <Collapsable>
    <div slot="above-fold">
      <h3 class="mb-s16">Affinez votre recherche</h3>
    </div>
    <div slot="under-fold">
      {#if numResults}
        <div class="text-gray-text-alt2 text-f14">
          {numResults} résultat{#if numResults > 1}s{/if}
        </div>
      {/if}
      <div class="border-t border-gray-01 my-s12" />
      <form on:submit|preventDefault={handleSearch}>
        <Field
          type="select"
          bind:value={category}
          onSelectChange={handleCategoryChange}
          placeholder="Choisissez"
          choices={catChoices}
          label="Thématique"
          vertical
          required
        />

        <Field
          type="select"
          bind:value={subcategory}
          placeholder="Choisissez"
          choices={subCatChoices}
          label="Besoin(s)"
          vertical
        />

        <Field type="custom" label="Lieu" required vertical>
          <CitySearch
            slot="custom-input"
            name="city"
            placeholder="Ville du bénéficiaire"
            initialValue={cityLabel}
            handleChange={(city) => {
              cityCode = city.properties.citycode;
              cityLabel = `${
                city.properties.label
              } (${getDepartmentFromCityCode(city.properties.postcode)})`;
            }}
          />
        </Field>

        <Button
          type="submit"
          label="Mettre à jour"
          disabled={!category || !cityCode}
          preventDefaultOnMouseDown
        />
      </form>
      <p class="mt-s16 text-gray-text-alt2 text-f12 text-center">
        Le service DORA est actuellement <a
          class="underline"
          target="_blank"
          rel="noopener"
          href="https://communaute.inclusion.beta.gouv.fr/t/mise-en-visibilite-de-loffre-dinsertion-lancement-de-dora/4090"
          >en construction</a
        >, et se concentre sur 3 thématiques de services (mobilité, garde
        d’enfant et hébergement/logement) et 3 territoires (Loire-Atlantique,
        Ardennes et La Réunion).
      </p>
    </div>
  </Collapsable>
</div>
