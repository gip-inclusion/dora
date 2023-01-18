<script lang="ts">
  import MultiSelectField from "$lib/components/inputs/multi-select-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { orderAndReformatSubcategories } from "$lib/utils/misc";
  import type { Schema } from "$lib/validation/schemas/utils";
  import InclusionNumSwitch from "./inclusion-num-switch.svelte";

  export let subcategories: string[] = [];
  export let servicesOptions: ServicesOptions, service: Service;
  export let schema: Schema;

  export let model: Model | undefined = undefined;
  export let isModel = false;
  const useModel = model != null;

  let isPristine = service.subcategories.length === 0;

  let previousCategories = [];

  function handleCategoriesChange(categories) {
    if (
      isPristine &&
      categories.length === 1 &&
      categories[0] === "numerique"
    ) {
      service.useInclusionNumeriqueScheme = true;
      isPristine = false;
    } else if (categories.length !== 1) {
      service.useInclusionNumeriqueScheme = false;
    }
    previousCategories = categories;

    subcategories = categories.length
      ? servicesOptions.subcategories.filter(({ value }) =>
          categories.some((cat) => value.startsWith(cat))
        )
      : [];

    subcategories = orderAndReformatSubcategories(
      subcategories,
      categories,
      servicesOptions
    );

    service.subcategories = service.subcategories.filter((scat) =>
      categories.some((cat) => scat.startsWith(cat))
    );
  }
</script>

<MultiSelectField
  id="categories"
  schema={schema.categories}
  bind:value={service.categories}
  choices={servicesOptions.categories}
  onChange={handleCategoriesChange}
  placeholderMulti="Sélectionner"
  sort
/>

{#if service.categories.includes("numerique") && !(isModel || useModel)}
  <InclusionNumSwitch bind:service />
{/if}
