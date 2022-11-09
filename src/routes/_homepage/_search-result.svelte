<script lang="ts">
  import { SERVICE_UPDATE_STATUS, type ServiceSearchResult } from "$lib/types";
  import UpdateStatusIcon from "$lib/components/services/icons/update-status.svelte";

  import {
    computeUpdateStatusData,
    computeUpdateStatusLabel,
  } from "$lib/utils/service";

  export let id: string;
  export let result: ServiceSearchResult;

  const updateStatusData = computeUpdateStatusData(result);
  const hasLocationTag = result.distance || result.location === "À distance";
</script>

<div {id} class="rounded-ml border border-gray-02 shadow-md" tabindex="-1">
  <div class="relative p-s32 pr-s64">
    <a
      href="/structures/{result.structure}"
      class="mb-s24 block text-f14 {hasLocationTag ? 'mt-s48 lg:mt-s0' : ''}"
    >
      {result.structureInfo.name}
    </a>

    <h3 class="mb-s0 text-france-blue lg:mb-s24">
      <a
        class="full-result-link hover:underline"
        href="/services/{result.slug}"
      >
        {result.name}
      </a>
    </h3>

    {#if hasLocationTag}
      <div
        class="absolute top-s32 rounded-xl bg-france-blue py-s4 px-s10 text-f14 font-bold text-white lg:right-s32"
      >
        {#if result.distance}
          à&nbsp;{result.distance}&nbsp;{result.distance > 1 ? "kms" : "km"}
        {/if}
        {#if result.location === "À distance"}
          À distance
        {/if}
      </div>
    {/if}

    <p class="relative z-10 mt-s16 hidden text-f16 text-gray-text md:block">
      <a href="/services/{result.slug}">{result.shortDesc}</a>
    </p>
  </div>

  <div class="border-t border-gray-02 p-s32 pr-s64 text-gray-text">
    <div class="flex">
      <span class="mr-s8 ">
        <UpdateStatusIcon
          updateStatus={SERVICE_UPDATE_STATUS.NOT_NEEDED}
          small
        />
      </span>
      {computeUpdateStatusLabel(updateStatusData)}
    </div>
  </div>
</div>

<style lang="postcss">
  /*
  * Link is on <h3> but we want all the card clickable (in an accessible way)
  * Source: http://inclusive-components.design/cards/
  */
  .full-result-link::after {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
  }
</style>
