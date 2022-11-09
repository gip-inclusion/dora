<script lang="ts">
  import { goto } from "$app/navigation";

  import Button from "$lib/components/button.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import { getDepartmentFromCityCode, moveToTheEnd } from "$lib/utils";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import { getQuery } from "./_search";
  import SelectField from "$lib/components/form/select/select-field.svelte";
  import type { FeeCondition, ServicesOptions } from "$lib/types";

  export let servicesOptions: ServicesOptions;
  export let categoryId: string;
  export let subCategoryId: string;
  export let cityCode: string;
  export let cityLabel: string;
  export let kindId: string | undefined = undefined;
  export let fee: FeeCondition[];

  function handleSearch() {
    const query = getQuery({
      categoryIds: [categoryId],
      subCategoryIds: [subCategoryId],
      cityCode,
      cityLabel,
      kindId,
      fee,
    });
    goto(`recherche?${query}`);
  }

  $: subCategoryChoices = moveToTheEnd(
    servicesOptions.subcategories.filter(
      ({ value }) => value.startsWith(categoryId),
      "label"
    )
  );

  function handleCategoryChange(cat) {
    subCategoryChoices = cat
      ? servicesOptions.subcategories.filter(({ value }) =>
          value.startsWith(cat)
        )
      : [];

    subCategoryChoices = moveToTheEnd(subCategoryChoices, "label", "Autre", {
      sortBeginning: true,
    });

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
      choices={servicesOptions.categories}
      label="Thématique"
      vertical
      required
      sortSelect
    />

    <Field
      type="select"
      bind:value={subCategoryId}
      placeholder="Sélectionner"
      choices={subCategoryChoices}
      label="Besoin"
      vertical
    />

    <Field type="custom" label="Lieu" required vertical>
      <CitySearch
        slot="custom-input"
        name="city"
        placeholder="Ville du bénéficiaire"
        initialValue={cityLabel}
        onChange={(city) => {
          cityCode = city?.code;
          cityLabel = `${city?.name} (${getDepartmentFromCityCode(
            city?.code
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

    <SelectField
      label="Frais à charge"
      name="fee"
      placeholder="Choississez"
      bind:value={fee}
      isMultiple
      choices={[...servicesOptions.feeConditions]}
    />

    <Button
      type="submit"
      label="Rechercher"
      disabled={!categoryId || !cityCode}
      preventDefaultOnMouseDown
    />
  </form>
</FieldSet>
