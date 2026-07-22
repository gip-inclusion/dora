<script lang="ts" module>
  import type {
    FeeCondition,
    LocationKind,
    ServiceCategory,
    ServiceKind,
  } from "$lib/types";

  // Variante mots-clés : mêmes filtres que la recherche par catégorie,
  // PLUS un filtre « Thématiques et besoins » (cf. `categories` ci-dessous),
  // la recherche par mots-clés n'ayant pas de catégorie présélectionnée.
  // MOINS les labels de financements.
  export interface Filters {
    categories: Array<ServiceCategory>;
    subCategories: Array<string>;
    diPublics: Array<string>;
    kinds: Array<ServiceKind>;
    feeConditions: Array<FeeCondition>;
    locationKinds: Array<LocationKind>;
  }
</script>

<script lang="ts">
  import type { ServicesOptions } from "$lib/types";

  // Atome de filtre réutilisé tel quel depuis le contrôle (non couplé à PageData).
  import ResultFilter from "../recherche/result-filter.svelte";

  interface Props {
    servicesOptions: ServicesOptions;
    filters: Filters;
  }

  let { servicesOptions, filters = $bindable() }: Props = $props();
  function getCategoryFromSubcategory(subcategory: string) {
    return subcategory.split("--")[0];
  }
</script>

<div class="gap-s32 flex flex-col">
  <ResultFilter
    id="categories"
    label="Thématiques"
    choices={servicesOptions.categories}
    bind:group={filters.categories}
  />
  {#if filters.categories.length}
    <ResultFilter
      id="subcategories"
      label="Besoins"
      choices={servicesOptions.subcategories.filter(({ value }) =>
        filters.categories
          .map((cat) => cat.toString())
          .includes(getCategoryFromSubcategory(value))
      )}
      bind:group={filters.subCategories}
    />
  {/if}
  <ResultFilter
    id="diPublics"
    label="Publics"
    choices={servicesOptions.diPublics}
    bind:group={filters.diPublics}
  />
  <ResultFilter
    id="kinds"
    label="Type de service"
    choices={servicesOptions.kinds}
    bind:group={filters.kinds}
  />
  <ResultFilter
    id="locationKinds"
    label="Lieu d’accueil"
    choices={servicesOptions.locationKinds}
    bind:group={filters.locationKinds}
  />
  <ResultFilter
    id="feeConditions"
    label="Frais à charge"
    choices={servicesOptions.feeConditions}
    bind:group={filters.feeConditions}
  />
</div>
