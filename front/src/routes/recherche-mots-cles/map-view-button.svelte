<!--
  Variante recherche par mots-clés de la carte « Voir sur la carte ».
  Reprend le contrôle, mais sans le libellé de ville (la recherche par mots-clés
  n'expose pas `cityLabel`).
-->
<script lang="ts">
  import mapViewImage from "$lib/assets/illustrations/map-view.jpg";

  import type { FundingLabel, ServiceSearchResult } from "$lib/types";
  import Button from "$lib/components/display/button.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";

  import type { PageData } from "./$types";
  import type { Filters } from "./result-filters.svelte";
  import ResultFilters from "./result-filters.svelte";
  import ResultMap from "./result-map.svelte";
  import SearchResults from "./search-results.svelte";

  interface Props {
    data: PageData;
    availableFundingLabels: Array<FundingLabel>;
    filters: Filters;
    services: ServiceSearchResult[];
    total: number;
  }

  let {
    data,
    availableFundingLabels,
    filters = $bindable(),
    services,
    total,
  }: Props = $props();

  let isMapViewOpen = $state(false);
  let isResultFiltersOpen = $state(false);
  let selectedServiceSlug: string | undefined = $state();

  function handleServiceClick(slug: string) {
    selectedServiceSlug = slug;
  }

  function handleCloseModal() {
    isMapViewOpen = false;
    isResultFiltersOpen = false;
    selectedServiceSlug = undefined;
  }
</script>

<div
  style={`background-image: url('${mapViewImage}'); height: 116px`}
  class="flex items-center justify-center rounded-2xl bg-cover"
>
  <Button label="Voir sur la carte" onclick={() => (isMapViewOpen = true)} />
  <Modal bind:isOpen={isMapViewOpen} hideTitle hideCloseButton noPadding>
    <div class="flex h-[90vh]">
      <div class="pb-s16 flex w-[448px] flex-col overflow-y-auto">
        <div
          class="top-s0 gap-s8 px-s32 pt-s32 sticky z-10 flex flex-col bg-white"
        >
          <Button label="Fermer la carte" onclick={handleCloseModal} />
          <Button
            label="Affiner la recherche"
            secondary
            onclick={() => (isResultFiltersOpen = true)}
          />
          <Modal
            title="Affiner la recherche"
            width="small"
            bind:isOpen={isResultFiltersOpen}
          >
            <ResultFilters
              servicesOptions={data.servicesOptions}
              {availableFundingLabels}
              bind:filters
            />
          </Modal>
          <div class="my-s24 text-f21">
            <strong>
              {total}
              {total > 1 ? "services" : "service"}</strong
            >
          </div>
        </div>
        <div class="gap-s24 px-s32 flex flex-col">
          {#if total}
            <SearchResults
              {data}
              {services}
              summarized
              noPagination
              {selectedServiceSlug}
              {total}
            />
          {/if}
        </div>
      </div>
      <div class="flex-1">
        <ResultMap {data} {services} onServiceClick={handleServiceClick} />
      </div>
    </div>
  </Modal>
</div>
