<script lang="ts">
  import { run } from 'svelte/legacy';

  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import type { Service, ServicesOptions } from "$lib/types";
  import { orderAndReformatSubcategories } from "$lib/utils/misc";

  interface Props {
    service: Service;
    servicesOptions: ServicesOptions;
    description?: string;
  }

  let { service = $bindable(), servicesOptions, description = "" }: Props = $props();

  let availableSubcategories = $state([]);

  run(() => {
    availableSubcategories = orderAndReformatSubcategories(
      service.categories.length
        ? servicesOptions.subcategories.filter(({ value }) =>
            service.categories.some((cat) => value.startsWith(cat))
          )
        : [],
      service.categories,
      servicesOptions
    );
  });
</script>

<MultiSelectField
  id="subcategories"
  bind:value={service.subcategories}
  choices={availableSubcategories}
  {description}
/>
