<script lang="ts">
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getCategoryLabel, getSubCategoryLabel } from "$lib/utils/service";

  import ServiceList from "./components/service-list.svelte";
  import ServiceSection from "./components/service-section.svelte";
  import ServiceSubsection from "./components/service-subsection.svelte";

  export let service: Service | Model;
  export let servicesOptions: ServicesOptions;

  $: categories = service.subcategories.reduce(
    (acc, subCategorySlug) => {
      const categorySlug = subCategorySlug.split("--")[0];
      return {
        ...acc,
        [categorySlug]: [...(acc[categorySlug] ?? []), subCategorySlug],
      };
    },
    {} as Record<string, string[]>
  );

  $: hasCategories = Object.keys(categories).length > 0;
  $: hasKinds = service.kinds && service.kinds.length > 0;
  $: hasSource = !service.isModel && !!service.source;

  $: hasOtherInformations = hasCategories || hasKinds || hasSource;
</script>

{#if hasOtherInformations}
  <ServiceSection title="Autres informations">
    {#if hasCategories}
      <ServiceSubsection title="Thématiques et besoins associés">
        <ServiceList>
          {#each Object.entries(categories) as [categorySlug, subCategorySlugs]}
            <li>
              <strong
                >{getCategoryLabel(
                  categorySlug,
                  servicesOptions
                )}&#8239;:</strong
              >
              {#each subCategorySlugs as subCategorySlug, index}
                <span
                  >{getSubCategoryLabel(
                    subCategorySlug,
                    servicesOptions
                  )}{index < subCategorySlugs.length - 1 ? ", " : ""}</span
                >
              {/each}
            </li>
          {/each}
        </ServiceList>
      </ServiceSubsection>
    {/if}
    {#if hasKinds}
      <ServiceSubsection title="Type de service">
        {service.kindsDisplay.join(", ")}
      </ServiceSubsection>
    {/if}
    {#if hasSource}
      <ServiceSubsection title="Source du service">
        Ce service provient de {!service.isModel ? service.source : ""} et est synchronisé
        via le référentiel data·inclusion.
      </ServiceSubsection>
    {/if}
  </ServiceSection>
{/if}
