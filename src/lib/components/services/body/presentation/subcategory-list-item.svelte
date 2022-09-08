<script lang="ts">
  import type { ServicesOptions } from "$lib/types";
  import {
    getCategoryLabel,
    getSubCategoryLabel,
    getCategoryIcon,
  } from "$lib/utils/service";

  export let subCategorySlug: string;
  export let servicesOptions: ServicesOptions;

  const categorySlug = subCategorySlug.split("--")[0];
</script>

<div
  class="inline-flex flex-wrap items-center rounded-md bg-service-blue-light py-s8 px-s16 text-f14 text-magenta-dark"
>
  <div class="mr-s4 inline-flex items-center self-start">
    <span class="mr-s8 inline-block h-s24 w-s24 fill-current text-france-blue">
      {@html getCategoryIcon(categorySlug)}
    </span>

    <strong>
      {getCategoryLabel(categorySlug, servicesOptions).toUpperCase()}
    </strong>
  </div>

  <span class="mr-s4">•</span>
  {getSubCategoryLabel(subCategorySlug, servicesOptions)}
</div>
