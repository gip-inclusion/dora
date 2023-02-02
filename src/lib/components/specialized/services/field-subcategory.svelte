<script lang="ts">
  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import type { Service, ServicesOptions } from "$lib/types";
  import { orderAndReformatSubcategories } from "$lib/utils/misc";

  export let service: Service;
  export let servicesOptions: ServicesOptions;

  let availableSubcategories = [];

  $: availableSubcategories = orderAndReformatSubcategories(
    service.categories.length
      ? servicesOptions.subcategories.filter(({ value }) =>
          service.categories.some((cat) => value.startsWith(cat))
        )
      : [],
    service.categories,
    servicesOptions
  );
</script>

<MultiSelectField
  id="subcategories"
  bind:value={service.subcategories}
  choices={availableSubcategories}
  placeholder="Sélectionner"
  placeholderMulti="Sélectionner"
/>
