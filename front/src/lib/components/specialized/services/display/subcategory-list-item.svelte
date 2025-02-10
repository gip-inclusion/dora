<script lang="ts">
  import { addIcon, substractIcon } from "$lib/icons";
  import type { ServicesOptions } from "$lib/types";
  import {
    getCategoryIcon,
    getCategoryLabel,
    getSubCategoryLabel,
  } from "$lib/utils/service";

  export let categorySlug: string;
  export let subCategorySlugs: string[];
  export let servicesOptions: ServicesOptions;

  let expanded = false;
</script>

<div class="text-f14 text-france-blue">
  <div
    class={`mr-s4 px-s16 py-s8 inline-flex items-center self-start rounded-lg ${expanded ? "bg-france-blue rounded-br-none rounded-bl-none text-white" : "bg-service-blue-light"}`}
  >
    <span class="mr-s8 h-s24 w-s24 inline-block fill-current">
      {@html getCategoryIcon(categorySlug)}
    </span>

    <strong>
      {getCategoryLabel(categorySlug, servicesOptions).toUpperCase()}
    </strong>

    <button
      class="ml-s10 h-s24 w-s24 fill-current print:hidden"
      on:click={() => (expanded = !expanded)}
    >
      {#if !expanded}
        {@html addIcon}
      {:else}
        {@html substractIcon}
      {/if}
    </button>
  </div>

  <div class:hidden={!expanded} class="w-full md:w-auto print:block!">
    <ul
      class="gap-s12 bg-service-blue-light p-s16 pr-s32 relative z-10 mt-[-1px] inline-flex w-full flex-col rounded-lg rounded-tl-none md:w-auto"
    >
      {#each subCategorySlugs as subCategorySlug}
        <li class="text-gray-dark md:min-w-[30rem]">
          {getSubCategoryLabel(subCategorySlug, servicesOptions)}
        </li>
      {/each}
    </ul>
  </div>
</div>
