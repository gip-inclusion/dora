<script lang="ts">
  import type { Service, ServicesOptions } from "$lib/types";
  import SubcategoryListItem from "./subcategory-list-item.svelte";

  export let service: Service;
  export let servicesOptions: ServicesOptions;

  let categoriesRecord: Record<string, string[]> = {};
  $: {
    categoriesRecord = {};

    service.subcategories.forEach((subCategorySlug) => {
      const category = subCategorySlug.split("--")[0];

      if (!categoriesRecord[category]) {
        categoriesRecord[category] = [];
      }
      categoriesRecord[category].push(subCategorySlug);
    });
  }
</script>

<div>
  {#each Object.entries(categoriesRecord) as [categorySlug, subCategorySlugs]}
    <div class="mb-s12">
      <SubcategoryListItem
        {categorySlug}
        {subCategorySlugs}
        {servicesOptions}
      />
    </div>
  {/each}
</div>
