<script>
  import { goto } from "$app/navigation";

  import Button from "$lib/components/button.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import { searchIcon } from "$lib/icons";

  export let servicesOptions;

  let category;
  let subcategory;
  let cityCode;

  function handleSearch() {
    goto(
      `recherche/?cat=${encodeURIComponent(category)}&sub=${encodeURIComponent(
        subcategory
      )}&city=${encodeURIComponent(cityCode)}`
    );
  }

  $: catChoices = servicesOptions.categories.map(([key, value]) => ({
    value: key,
    label: value,
  }));

  $: subCatChoices = servicesOptions.subCategories
    .filter(([key, _value]) => key.startsWith(category))
    .map(([key, value]) => ({
      value: key,
      label: value,
    }));
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
    color: var(--col-text-alt2);
    font-size: var(--f12);
  }
</style>

<div class="wrapper">
  <form on:submit|preventDefault={handleSearch}>
    <Field
      type="select"
      bind:value={category}
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
      label="Trouver"
      icon={searchIcon}
      iconOnLeft
      horizontalBottom
      small />
  </form>
  <p>
    Le service DORA est actuellement en construction, et se concentre sur 3
    thématiques de services (mobilité, garde d’enfant et hébergement/logement)
    et 2 territoires (Loire-Atlantique et Ardennes).
  </p>
</div>
