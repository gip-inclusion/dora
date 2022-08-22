<script lang="ts">
  import Breadcrumb from "$lib/components/breadcrumb.svelte";
  import { emotionHappyIcon, closeCircleFillIcon } from "$lib/icons";
  import type { Service } from "$lib/types";
  import { capitalize } from "$lib/utils";

  export let service: Service;
</script>

<div id="service-header" class="gap-s16 lg:flex-row-reverse lg:justify-between">
  <div class="mb-s48">
    <Breadcrumb
      {service}
      structure={service.structureInfo}
      currentLocation="service"
    />
  </div>
  <h1 class="mb-s14 text-f45 leading-[3rem] text-white print:text-france-blue">
    {service.name}
  </h1>

  <div
    class="mb-s48 flex flex-col text-f18 text-white print:text-france-blue md:flex-row md:items-center"
  >
    <div><strong>{capitalize(service.structureInfo.name)}</strong></div>
    <div class="mx-s8 hidden font-bold md:block" aria-hidden="true">•</div>
    <div>
      <a class="underline" href="/structures/{service.structureInfo.slug}"
        >Voir les autres services ({service.structureInfo.numServices})</a
      >
    </div>
  </div>

  <div
    class="mb-s32 flex flex-col text-f18  text-white print:text-france-blue md:flex-row md:items-center"
  >
    <div id="service-availability" class="mb-s10 flex items-center md:mb-s0">
      {#if service.isAvailable}
        <div
          class="mr-s8 h-s32 w-s32 fill-current text-service-available print:text-service-available-dark"
        >
          {@html emotionHappyIcon}
        </div>

        <span class="text-service-available print:text-service-available-dark"
          >Service disponible</span
        >
      {:else}
        <div
          class="mr-s8 h-s32 w-s32 fill-current text-service-unavailable print:text-service-unavailable-dark"
        >
          {@html closeCircleFillIcon}
        </div>
        <span class="text-service-unavailable">Service indisponible</span>
      {/if}
    </div>
    <div class="mx-s8 hidden font-bold md:block" aria-hidden="true">•</div>
    <div>
      Périmètre : <strong>{service.diffusionZoneDetailsDisplay}</strong>
    </div>
  </div>
</div>
