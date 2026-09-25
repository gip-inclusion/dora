<script lang="ts">
  import { getCategoryLabel, getSubCategoryLabel } from "$lib/utils/service";

  import type { Model, Service, ServicesOptions } from "$lib/types";

  interface Props {
    service: Service | Model;
    servicesOptions: ServicesOptions;
  }

  const { service, servicesOptions }: Props = $props();

  let categories = $derived(
    service.subcategories.reduce(
      (acc, subCategorySlug) => {
        const categorySlug = subCategorySlug.split("--")[0];
        return {
          ...acc,
          [categorySlug]: [...(acc[categorySlug] ?? []), subCategorySlug],
        };
      },
      {} as Record<string, string[]>
    )
  );
</script>

<section
  class="border-gray-02 p-s32 gap-s24 text-f16 text-gray-text [&_p]:mb-s0 [&_p]:text-f16 flex flex-col rounded-2xl border leading-24 [&_p]:leading-24"
>
  <div>
    <h3 class="text-f17 text-france-blue mb-s16 leading-24">
      Thématiques et besoins associés
    </h3>
    <div class="gap-s4 flex flex-col">
      {#each Object.entries(categories) as [categorySlug, subCategorySlugs]}
        <p>
          <strong class="text-gray-dark"
            >{getCategoryLabel(categorySlug, servicesOptions)}&#8239;:</strong
          >
          {subCategorySlugs
            .map((slug) => getSubCategoryLabel(slug, servicesOptions))
            .join(", ")}
        </p>
      {/each}
    </div>
  </div>

  {#if service.kind}
    <div>
      <h3 class="text-f17 text-france-blue mb-s16 leading-24">
        Type de service
      </h3>
      <p>{service.kindDisplay}</p>
    </div>
  {/if}

  {#if service.fundingLabelsDisplay?.length}
    <hr class="border-gray-02 my-s8" />

    <div>
      <h3 class="text-f17 text-france-blue mb-s16 leading-24">
        Service financé par
      </h3>
      <p>{service.fundingLabelsDisplay.join(" · ")}</p>
    </div>
  {/if}
</section>
