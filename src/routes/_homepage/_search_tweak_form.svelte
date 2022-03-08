<script>
  import { goto } from "$app/navigation";

  import Button from "$lib/components/button.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import { getDepartmentFromCityCode } from "$lib/utils";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import { getQuery } from "./_search";

  export let servicesOptions;
  export let categoryId;
  export let subCategoryId;
  export let cityCode;
  export let cityLabel;
  export let kindId = undefined;
  export let hasNoFees = undefined;

  function handleSearch() {
    const query = getQuery({
      categoryId,
      subCategoryId,
      cityCode,
      cityLabel,
      kindId,
      hasNoFees,
    });
    goto(`recherche?${query}`);
  }

  $: catChoices = servicesOptions.categories.map((choice) => {
    if (
      [
        "GL",
        "FL",
        "CR",
        "FI",
        "IL",
        "DI",
        "FA",
        "RE",
        "RI",
        "EQ",
        "HE",
        "HA",
        "JO",
      ].includes(choice.value)
    ) {
      choice.tags = ["nouv."];
    }
    return choice;
  });

  $: subCatChoices = servicesOptions.subcategories.filter(({ value }) =>
    value.startsWith(categoryId)
  );

  function handleCategoryChange(cat) {
    subCatChoices = cat
      ? servicesOptions.subcategories.filter(({ value }) =>
          value.startsWith(cat)
        )
      : [];

    if (cat && subCategoryId && !subCategoryId.startsWith(cat))
      subCategoryId = null;
  }
</script>

<FieldSet
  title="Filtres"
  description="Affinez votre recherche."
  noTopPadding
  collapsable
>
  <form on:submit|preventDefault={handleSearch} class="flex flex-col gap-s16">
    <Field
      type="select"
      bind:value={categoryId}
      onSelectChange={handleCategoryChange}
      placeholder="Sélectionner"
      choices={catChoices}
      label="Thématique"
      vertical
      required
      sortSelect
    />

    <Field
      type="select"
      bind:value={subCategoryId}
      placeholder="Sélectionner"
      choices={subCatChoices}
      label="Besoin"
      vertical
      sortSelect
    />

    <Field type="custom" label="Lieu" required vertical>
      <CitySearch
        slot="custom-input"
        name="city"
        placeholder="Ville du bénéficiaire"
        initialValue={cityLabel}
        handleChange={(city) => {
          cityCode = city?.properties.citycode;
          cityLabel = `${city?.properties.label} (${getDepartmentFromCityCode(
            city?.properties.postcode
          )})`;
        }}
      />
    </Field>

    <Field
      type="select"
      bind:value={kindId}
      placeholder="Sélectionner"
      choices={servicesOptions.kinds}
      label="Type"
      vertical
      sortSelect
    />

    <Field type="toggle" label="Sans frais à charge" bind:value={hasNoFees} />

    <Button
      type="submit"
      label="Rechercher"
      disabled={!categoryId || !cityCode}
      preventDefaultOnMouseDown
    />
  </form>
</FieldSet>
