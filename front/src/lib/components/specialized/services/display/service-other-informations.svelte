<script lang="ts">
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getCategoryLabel, getSubCategoryLabel } from "$lib/utils/service";

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
  <section class="gap-s24 text-gray-text flex flex-col">
    <h2 class="text-f23 text-france-blue mb-s0 leading-32 font-bold">
      Autres informations
    </h2>
    {#if hasCategories}
      <section>
        <h3 class="text-f17 leading-s24 text-gray-dark mb-s8 font-bold">
          Thématiques et besoins associés
        </h3>
        <ul class="space-y-s2 list-inside list-disc">
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
        </ul>
      </section>
    {/if}
    {#if hasKinds}
      <section>
        <h3 class="text-f17 leading-s24 text-gray-dark mb-s8 font-bold">
          Type de service
        </h3>
        <ul
          class="[&>li+li]:before:mx-s6 [&>li]:inline [&>li+li]:before:content-['•']"
        >
          {#each service.kindsDisplay as kind}
            <li>{kind}</li>
          {/each}
        </ul>
      </section>
    {/if}
    {#if hasSource}
      <section>
        <h3 class="text-f17 leading-s24 text-gray-dark mb-s8 font-bold">
          Source du service
        </h3>
        <div>
          Ce service provient de {!service.isModel ? service.source : ""} et est
          synchronisé via le référentiel data·inclusion.
        </div>
      </section>
    {/if}
  </section>
{/if}
