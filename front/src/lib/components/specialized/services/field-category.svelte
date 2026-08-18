<script lang="ts">
  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service | Model;
    description?: string;
  }

  let {
    servicesOptions,
    service = $bindable(),
    description = "",
  }: Props = $props();

  function handleCategoriesChange(categories) {
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
  sort
  {description}
/>
