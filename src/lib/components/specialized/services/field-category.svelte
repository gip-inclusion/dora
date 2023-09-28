<script lang="ts">
  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import InclusionNumSwitch from "./inclusion-num-switch.svelte";

  export let servicesOptions: ServicesOptions, service: Service;

  export let model: Model | undefined = undefined;
  export let isModel = false;
  export let description = "";
  const useModel = model != null;

  function handleCategoriesChange(categories) {
    if (
      service.categories.length === 0 &&
      categories.length === 1 &&
      categories[0] === "numerique"
    ) {
      service.useInclusionNumeriqueScheme = true;
    }
    if (categories.length !== 1) {
      service.useInclusionNumeriqueScheme = false;
    }
    service.categories = categories;

    service.subcategories = service.subcategories.filter((scat) =>
      categories.some((cat) => scat.startsWith(cat))
    );
  }
</script>

<MultiSelectField
  id="categories"
  value={service.categories}
  choices={servicesOptions.categories}
  onChange={handleCategoriesChange}
  placeholder="Sélectionner"
  placeholderMulti="Sélectionner"
  sort
  {description}
/>

{#if service.categories.includes("numerique") && !(isModel || useModel)}
  <InclusionNumSwitch bind:service />
{/if}
