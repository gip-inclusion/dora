<!--
  Variante recherche par mots-clés de la carte « Voir sur la carte ».
  Reprend le contrôle, mais sans le libellé de ville (la recherche par mots-clés
  n'expose pas `cityLabel`).
-->
<script lang="ts">
  import { browser } from "$app/environment";

  import mapViewImage from "$lib/assets/illustrations/map-view.jpg";

  import type { ServiceSearchResult } from "$lib/types";
  import Button from "$lib/components/display/button.svelte";
  import Pagination from "$lib/components/display/pagination.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";

  import type { PageData } from "./$types";
  import ResultMap from "./result-map.svelte";
  import SearchResults from "./search-results.svelte";

  interface Props {
    data: PageData;
    services: ServiceSearchResult[];
    total: number;
    pages: number;
    current: number;
    onPageChange: (page: number) => void;
  }

  let { data, services, total, pages, current, onPageChange }: Props = $props();

  let isMapViewOpen = $state(false);
  let selectedServiceSlug: string | undefined = $state();
  let resultsColumn: HTMLDivElement | undefined = $state();

  function handleServiceClick(slug: string) {
    selectedServiceSlug = slug;
  }

  function handleCloseModal() {
    isMapViewOpen = false;
    selectedServiceSlug = undefined;
  }
</script>

<div
  style={`background-image: url('${mapViewImage}'); height: 116px`}
  class="flex items-center justify-center rounded-2xl bg-cover"
>
  <Button label="Voir sur la carte" onclick={() => (isMapViewOpen = true)} />
  {#if browser}
    <Modal bind:isOpen={isMapViewOpen} hideTitle hideCloseButton noPadding>
      <div class="flex h-[90vh]">
        <div
          bind:this={resultsColumn}
          class="pb-s16 flex w-[448px] flex-col overflow-y-auto"
        >
          <div
            class="top-s0 gap-s8 px-s32 pt-s32 sticky z-10 flex flex-col bg-white"
          >
            <Button label="Fermer la carte" onclick={handleCloseModal} />
            <div class="my-s8 text-f21">
              <strong>
                {total}
                {total > 1 ? "services" : "service"}</strong
              >
            </div>
          </div>
          <div class="gap-s24 flex flex-col">
            {#if total}
              <div class="px-s32">
                <SearchResults
                  {data}
                  {services}
                  summarized
                  {selectedServiceSlug}
                />
              </div>
              <Pagination
                {current}
                totalPages={pages}
                onPageChange={(activePage) => {
                  resultsColumn?.scrollTo({ top: 0 });
                  onPageChange(activePage);
                }}
              />
            {/if}
          </div>
        </div>
        <div class="flex-1">
          <ResultMap {data} {services} onServiceClick={handleServiceClick} />
        </div>
      </div>
    </Modal>
  {/if}
</div>
