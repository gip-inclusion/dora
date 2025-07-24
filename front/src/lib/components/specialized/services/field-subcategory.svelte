<script lang="ts">
  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { orderAndReformatSubcategories } from "$lib/utils/misc";

  interface Props {
    service: Service | Model;
    servicesOptions: ServicesOptions;
    description?: string;
  }

  let {
    service = $bindable(),
    servicesOptions,
    description = "",
  }: Props = $props();

  let availableSubcategories = $derived(
    orderAndReformatSubcategories(
      service.categories.length
        ? servicesOptions.subcategories.filter(({ value }) =>
            service.categories.some((cat) => value.startsWith(cat))
          )
        : [],
      service.categories,
      servicesOptions
    )
  );
</script>

<MultiSelectField
  id="subcategories"
  bind:value={service.subcategories}
  choices={availableSubcategories}
  {description}
/>
