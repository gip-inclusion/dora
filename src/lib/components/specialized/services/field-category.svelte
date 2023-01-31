<script lang="ts">
  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import InclusionNumSwitch from "./inclusion-num-switch.svelte";

  export let servicesOptions: ServicesOptions, service: Service;

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

    service.subcategories = service.subcategories.filter((scat) =>
      categories.some((cat) => scat.startsWith(cat))
    );
  }
</script>

<MultiSelectField
  id="categories"
  bind:value={service.categories}
  choices={servicesOptions.categories}
  onChange={handleCategoriesChange}
  placeholder="Sélectionner"
  placeholderMulti="Sélectionner"
  sort
/>

{#if service.categories.includes("numerique") && !(isModel || useModel)}
  <InclusionNumSwitch bind:service />
{/if}
