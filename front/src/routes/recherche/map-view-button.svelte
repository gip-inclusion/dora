<script lang="ts">
  import mapViewImage from "$lib/assets/illustrations/map-view.jpg";

  import type { FundingLabel, ServiceSearchResult } from "$lib/types";
  import Button from "$lib/components/display/button.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";

  import type { PageData } from "./$types";
  import type { Filters } from "./result-filters.svelte";
  import ResultCount from "./result-count.svelte";
  import ResultFilters from "./result-filters.svelte";
  import SearchResults from "./search-results.svelte";
  import ResultMap from "./result-map.svelte";

  interface Props {
    data: PageData;
    availableFundingLabels: Array<FundingLabel>;
    filters: Filters;
    filteredServices: ServiceSearchResult[];
  }

  let {
    data,
    availableFundingLabels,
    filters = $bindable(),
    filteredServices,
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
  <Button label="Voir sur la carte" on:click={() => (isMapViewOpen = true)} />
  <Modal bind:isOpen={isMapViewOpen} hideTitle hideCloseButton noPadding>
    <div class="flex h-[90vh]">
      <div class="pb-s16 flex w-[448px] flex-col overflow-y-auto">
        <div
          class="top-s0 gap-s8 px-s32 pt-s32 sticky z-10 flex flex-col bg-white"
        >
          <Button label="Fermer la carte" on:click={handleCloseModal} />
          <Button
            label="Affiner la recherche"
            secondary
            on:click={() => (isResultFiltersOpen = true)}
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
          <div class="my-s24">
            <ResultCount
              resultCount={filteredServices.length}
              cityLabel={data.cityLabel}
            />
          </div>
        </div>
        <div class="gap-s24 px-s32 flex flex-col">
          {#if filteredServices.length}
            <SearchResults
              {data}
              {filters}
              {filteredServices}
              summarized
              noAlertButtonBottomGap
              noPagination
              {selectedServiceSlug}
            />
          {/if}
        </div>
      </div>
      <div class="flex-1">
        <ResultMap
          {data}
          {filteredServices}
          onServiceClick={handleServiceClick}
        />
      </div>
    </div>
  </Modal>
</div>
