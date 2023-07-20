<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import type { Service, ServicesOptions } from "$lib/types";
  import SubcategoryListItem from "./subcategory-list-item.svelte";

  export let service: Service;
  export let servicesOptions: ServicesOptions;

  const numberOfSubcategories = 3;
  let expanded = false;

  $: subcategories = expanded
    ? service.subcategories
    : service.subcategories?.slice(0, numberOfSubcategories);
</script>

<ul>
  {#if Array.isArray(service.subcategories)}
    {#each subcategories as subCategory, i (subCategory)}
      <li class="mb-s8">
        <SubcategoryListItem subCategorySlug={subCategory} {servicesOptions} />
      </li>
    {/each}
  {:else}
    <li class="text-f18 text-gray-text">Non renseigné</li>
  {/if}
</ul>

{#if !expanded && service.subcategories?.length > numberOfSubcategories}
  <Button
    label="Voir tous les besoins"
    on:click={() => (expanded = true)}
    noBackground
    small
    noPadding
    hoverUnderline
  />
{/if}
