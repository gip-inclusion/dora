<script lang="ts">
  import { getCategoryLabel, getSubCategoryLabel } from "$lib/utils/service";

  import type { Model, Service, ServicesOptions } from "$lib/types";

  import ServiceCard from "./components/service-card.svelte";
  import ServiceCardBlock from "./components/service-card-block.svelte";

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

<ServiceCard>
  <ServiceCardBlock title="Thématiques et besoins associés">
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
  </ServiceCardBlock>

  {#if service.kind}
    <ServiceCardBlock title="Type de service">
      <p>{service.kindDisplay}</p>
    </ServiceCardBlock>
  {/if}

  {#if service.fundingLabelsDisplay?.length}
    <hr class="border-gray-02 my-s8" />

    <ServiceCardBlock title="Service financé par">
      <p>{service.fundingLabelsDisplay.join(" · ")}</p>
    </ServiceCardBlock>
  {/if}
</ServiceCard>
