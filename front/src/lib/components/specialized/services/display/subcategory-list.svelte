<script lang="ts">
  import type { Service, ServicesOptions } from "$lib/types";
  import SubcategoryListItem from "./subcategory-list-item.svelte";

  export let service: Service;
  export let servicesOptions: ServicesOptions;

  let categoriesRecord: Record<string, string[]> = {};
  $: hasCategoriesInfos =
    service.subcategories != null && service.categories != null;
  $: {
    categoriesRecord = {};

    service.subcategories?.forEach((subCategorySlug) => {
      const category = subCategorySlug.split("--")[0];

      if (!categoriesRecord[category]) {
        categoriesRecord[category] = [];
      }
      categoriesRecord[category].push(subCategorySlug);
    });
  }
</script>

<div>
  {#if !hasCategoriesInfos}
    <ul class="text-f16 text-gray-text"><li>Non renseigné</li></ul>
  {:else}
    {#each Object.entries(categoriesRecord) as [categorySlug, subCategorySlugs]}
      <div class="mb-s12">
        <SubcategoryListItem
          {categorySlug}
          {subCategorySlugs}
          {servicesOptions}
        />
      </div>
    {/each}
  {/if}
</div>
