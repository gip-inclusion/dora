<script lang="ts" context="module">
  import { FUNDED_SERVICES } from "$lib/consts";
  import type { FeeCondition, LocationKind, ServiceKind } from "$lib/types";

  export type FundedByDepartment = keyof typeof FUNDED_SERVICES;

  interface FundedByOption {
    value: FundedByDepartment;
    label: string;
  }

  export type FundedByOptions = Array<FundedByOption>;

  export interface Filters {
    kinds: Array<ServiceKind>;
    fundedBy: Array<FundedByDepartment>;
    feeConditions: Array<FeeCondition>;
    locationKinds: Array<LocationKind>;
  }
</script>

<script lang="ts">
  import type { ServicesOptions } from "$lib/types";

  import ResultFilter from "./result-filter.svelte";

  export let servicesOptions: ServicesOptions;
  export let fundedByOptions: FundedByOptions;
  export let filters: Filters;
</script>

<div class="flex flex-col gap-s32">
  <ResultFilter
    id="kinds"
    label="Type de service"
    choices={servicesOptions.kinds}
    bind:group={filters.kinds}
  />
  {#key fundedByOptions}
    {#if fundedByOptions.length > 0}
      <ResultFilter
        id="fundedBy"
        label="Financé par"
        choices={fundedByOptions}
        bind:group={filters.fundedBy}
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
