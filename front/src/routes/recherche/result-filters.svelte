<script lang="ts" context="module">
  import type {
    FeeCondition,
    FundingLabel,
    LocationKind,
    ServiceKind,
  } from "$lib/types";

  export interface Filters {
    kinds: Array<ServiceKind>;
    fundingLabels: Array<FundingLabel["value"]>;
    feeConditions: Array<FeeCondition>;
    locationKinds: Array<LocationKind>;
  }
</script>

<script lang="ts">
  import type { ServicesOptions } from "$lib/types";

  import ResultFilter from "./result-filter.svelte";

  export let servicesOptions: ServicesOptions;
  export let availableFundingLabels: Array<FundingLabel>;
  export let filters: Filters;
</script>

<div class="gap-s32 flex flex-col">
  <ResultFilter
    id="kinds"
    label="Type de service"
    choices={servicesOptions.kinds}
    bind:group={filters.kinds}
  />
  {#key availableFundingLabels}
    {#if availableFundingLabels.length > 0}
      <ResultFilter
        id="fundingLabels"
        label="Financé par"
        choices={availableFundingLabels}
        bind:group={filters.fundingLabels}
      />
    {/if}
  {/key}
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
