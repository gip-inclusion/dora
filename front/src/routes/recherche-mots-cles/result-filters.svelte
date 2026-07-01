<script lang="ts" module>
  import type {
    FeeCondition,
    FundingLabel,
    LocationKind,
    ServiceCategory,
    ServiceKind,
  } from "$lib/types";

  // Variante mots-clés : mêmes filtres que la recherche par catégorie,
  // PLUS un filtre « Thématiques et besoins » (cf. `categories` ci-dessous),
  // la recherche par mots-clés n'ayant pas de catégorie présélectionnée.
  export interface Filters {
    categories: Array<ServiceCategory>;
    diPublics: Array<string>;
    kinds: Array<ServiceKind>;
    fundingLabels: Array<FundingLabel["value"]>;
    feeConditions: Array<FeeCondition>;
    locationKinds: Array<LocationKind>;
    page: number[];
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
</script>

<div class="gap-s32 flex flex-col">
  <ResultFilter
    id="categories"
    label="Thématiques et besoins"
    choices={servicesOptions.categories}
    bind:group={filters.categories}
  />
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
